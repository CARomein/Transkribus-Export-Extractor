import os
import csv
import shutil
from pathlib import Path

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
                
                print(f"Processing: {transkribus_id} -> {human_name}")
                shutil.move(str(human_folder), str(temp_destination))
                
                # Remove empty Transkribus ID folder
                item.rmdir()
            
            elif len(subfolders) == 0:
                print(f"Warning: Empty Transkribus ID folder: {transkribus_id}")
            else:
                print(f"Warning: Multiple subfolders in {transkribus_id}: {[f.name for f in subfolders]}")
    
    # Write CSV mapping
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Transkribus ID', 'Folder Name'])
        writer.writerows(sorted(mapping_data, key=lambda x: int(x[0])))
    
    print(f"\nMapping saved to: {csv_path}")
    
    # Move folders back from temporary directory to main export folder
    for item in temp_dir.iterdir():
        destination = export_path / item.name
        shutil.move(str(item), str(destination))
    
    # Remove temporary directory
    temp_dir.rmdir()
    
    print(f"\nRestructuring complete. Processed {len(mapping_data)} folders.")
    print(f"All folders now directly under: {export_path}")

if __name__ == "__main__":
    # Specify the path to your unpacked export_job_[number] folder
    export_folder = input("Enter the path to your export_job folder: ").strip()
    
    if os.path.exists(export_folder):
        process_transkribus_export(export_folder)
    else:
        print(f"Error: Path not found: {export_folder}")
