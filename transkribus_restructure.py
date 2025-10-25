import os
import csv
import shutil
import time
from pathlib import Path

def safe_rmdir(path, max_attempts=3):
    """
    Safely remove a directory with retry logic for Windows.
    
    Args:
        path: Path object to remove
        max_attempts: Number of retry attempts
    """
    for attempt in range(max_attempts):
        try:
            # Check if directory is truly empty (excluding hidden files we can't control)
            contents = list(path.iterdir())
            if contents:
                print(f"  Warning: Directory not empty, contains: {[str(f.name) for f in contents]}")
                # Try to remove any remaining contents
                for item in contents:
                    try:
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                    except Exception as e:
                        print(f"  Could not remove {item.name}: {e}")
            
            # Attempt to remove the directory
            path.rmdir()
            return True
            
        except PermissionError:
            if attempt < max_attempts - 1:
                print(f"  Retry {attempt + 1}/{max_attempts - 1}: Waiting for file system...")
                time.sleep(0.5)
            else:
                print(f"  Warning: Could not remove directory {path.name} - you may need to delete it manually")
                return False
        except Exception as e:
            print(f"  Warning: Error removing {path.name}: {e}")
            return False
    
    return False

def process_transkribus_export(export_path):
    """
    Process Transkribus export: create ID mapping and restructure folders.
    
    Args:
        export_path: Path to the unpacked export_job_[number] folder
    """
    export_path = Path(export_path)
    
    # Prepare output CSV
    csv_path = export_path / 'transkribus_id_mapping.csv'
    mapping_data = []
    
    # Temporary directory for moving folders
    temp_dir = export_path / '_temp_restructure'
    temp_dir.mkdir(exist_ok=True)
    
    print("Scanning Transkribus export structure...")
    
    # Track folders that couldn't be removed
    failed_removals = []
    
    # Iterate through Transkribus ID folders
    for item in export_path.iterdir():
        if item.is_dir() and item.name.isdigit():
            transkribus_id = item.name
            
            # Find the human-readable folder inside
            subfolders = [f for f in item.iterdir() if f.is_dir()]
            
            if len(subfolders) == 1:
                human_folder = subfolders[0]
                human_name = human_folder.name
                
                # Add to mapping
                mapping_data.append([transkribus_id, human_name])
                
                # Move to temporary location
                temp_destination = temp_dir / human_name
                
                # Handle naming conflicts
                counter = 1
                original_name = human_name
                while temp_destination.exists():
                    human_name = f"{original_name}_{counter}"
                    temp_destination = temp_dir / human_name
                    counter += 1
                    # Update mapping with new name if conflict occurred
                    mapping_data[-1][1] = human_name
                
                print(f"Processing: {transkribus_id} -> {human_name}")
                
                try:
                    shutil.move(str(human_folder), str(temp_destination))
                    
                    # Attempt to remove empty Transkribus ID folder
                    if not safe_rmdir(item):
                        failed_removals.append(transkribus_id)
                    
                except Exception as e:
                    print(f"  Error moving folder: {e}")
                    # If move failed, don't add to mapping
                    mapping_data.pop()
            
            elif len(subfolders) == 0:
                print(f"Warning: Empty Transkribus ID folder: {transkribus_id}")
                # Try to remove empty folder
                safe_rmdir(item)
            else:
                print(f"Warning: Multiple subfolders in {transkribus_id}: {[f.name for f in subfolders]}")
    
    # Write CSV mapping with semicolon delimiter for Dutch Excel
    if mapping_data:
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['Transkribus ID', 'Folder Name'])
            writer.writerows(sorted(mapping_data, key=lambda x: int(x[0])))
        
        print(f"\nMapping saved to: {csv_path}")
        print(f"Format: UTF-8 with BOM, semicolon-delimited (Excel compatible)")
    
    # Move folders back from temporary directory to main export folder
    print("\nMoving folders to final location...")
    for item in temp_dir.iterdir():
        destination = export_path / item.name
        try:
            shutil.move(str(item), str(destination))
            print(f"Moved: {item.name}")
        except Exception as e:
            print(f"Error moving {item.name}: {e}")
    
    # Remove temporary directory
    try:
        temp_dir.rmdir()
    except Exception as e:
        print(f"Warning: Could not remove temporary directory: {e}")
    
    # Summary
    print(f"\nRestructuring complete. Processed {len(mapping_data)} folders.")
    print(f"All folders now directly under: {export_path}")
    
    if failed_removals:
        print(f"\nNote: {len(failed_removals)} empty Transkribus ID folders could not be removed automatically:")
        for folder_id in failed_removals:
            print(f"  - {folder_id}")
        print("You may delete these manually if desired.")

if __name__ == "__main__":
    # Specify the path to your unpacked export_job_[number] folder
    export_folder = input("Enter the path to your export_job folder: ").strip()
    
    # Remove quotes if user pastes path with quotes
    export_folder = export_folder.strip('"').strip("'")
    
    if os.path.exists(export_folder):
        try:
            process_transkribus_export(export_folder)
        except KeyboardInterrupt:
            print("\n\nProcess interrupted by user.")
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"Error: Path not found: {export_folder}")
