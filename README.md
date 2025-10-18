# Transkribus Export Restructuring Tool

A Python utility for processing Transkribus exports by eliminating intermediary directory layers and documenting the relationship between Transkribus internal identifiers and user-defined folder names. This tool transforms the nested directory structure created by Transkribus into a flattened hierarchy that preserves meaningful folder names and facilitates subsequent analysis whilst simultaneously generating a CSV mapping file that records the correspondence between numerical identifiers and their associated collections.

## Purpose

Transkribus exports present a structural challenge for researchers working with multiple collections. When Transkribus prepares data for export, it organises materials within a compressed archive named according to the pattern `export_job_[number]`. Upon extraction, this archive reveals a series of directories named with numerical identifiers that correspond to Transkribus's internal collection management system. Each numerical directory contains a single subdirectory bearing the human-readable name originally assigned to that collection by the researcher. This arrangement creates an unnecessary hierarchical layer that obscures the meaningful collection names and complicates navigation through exported materials.

The restructuring tool addresses this problem by removing the intermediary numerical directories and relocating all user-named collections directly beneath the main export directory. This flattening operation transforms an opaque nested structure into an immediately comprehensible organisation that reflects the researcher's original naming conventions. Simultaneously, the tool preserves the relationship between Transkribus identifiers and collection names by generating a CSV file that documents these correspondences. This mapping file serves as a reference for troubleshooting, enables correlation between exported materials and collections visible in the Transkribus interface, and provides a record of the relationship between external and internal identifiers.

The tool is designed for researchers who have exported multiple collections from Transkribus and require efficient access to their materials without navigating through layers of numerical directories. By automating the restructuring process, the tool eliminates manual directory manipulation and ensures consistent handling of naming conflicts that may arise when multiple collections share identical names.

## Features

The restructuring tool provides several capabilities designed to streamline post-export processing. The tool automatically scans the export directory to identify all numerical subdirectories representing Transkribus collection identifiers. For each identified collection, it extracts the user-defined folder name nested within the numerical directory and records this correspondence. The tool generates a CSV file containing two columns: the Transkribus identifier and the associated folder name, sorted numerically by identifier for ease of reference.

After documenting the mappings, the tool relocates all user-named folders to the root of the export directory, removing the now-empty numerical directories. This restructuring operation handles naming conflicts gracefully by appending numerical suffixes to duplicate folder names, ensuring that no data is lost when multiple collections share the same user-defined name. The tool provides comprehensive progress reporting throughout execution, displaying each collection being processed and alerting the researcher to any anomalous structures such as empty numerical directories or directories containing multiple subfolders.

The restructuring process operates in place, modifying the existing directory structure rather than creating copies. This approach conserves storage space and ensures that researchers work with a single definitive version of their exported materials. All operations preserve the complete internal structure of each collection, including subdirectories, files, and the hierarchical relationships between them.

## Requirements

The tool requires Python 3.6 or higher. The script relies exclusively on standard library modules and requires no additional dependencies. The modules pathlib, shutil, csv, and os are included with all Python installations and need not be installed separately.

## Installation

Download the script and place `transkribus_restructure.py` in your working directory. The script can be executed from any location, as it prompts for the path to the export directory during runtime. No configuration files or environmental variables need be established prior to execution.

## Directory Structure

Before executing the restructuring script, researchers must first extract the Transkribus export archive. The typical workflow begins with downloading a file named `export_job_[number].zip` from Transkribus. Extracting this archive creates a directory bearing the same name, containing a series of subdirectories identified by numerical values. A representative pre-restructuring structure appears as follows:

```
export_job_123456/
├── 789012/
│   └── CollectionNameOne/
│       ├── page/
│       │   └── [PageXML files]
│       └── [other subdirectories and files]
├── 789013/
│   └── CollectionNameTwo/
│       ├── page/
│       │   └── [PageXML files]
│       └── [other subdirectories and files]
└── 789014/
    └── CollectionNameThree/
        ├── page/
        │   └── [PageXML files]
        └── [other subdirectories and files]
```

The numerical directories (789012, 789013, 789014, and so forth) represent Transkribus's internal collection identifiers. Each such directory contains exactly one subdirectory bearing the name originally assigned by the researcher. The restructuring tool transforms this arrangement by moving CollectionNameOne, CollectionNameTwo, and CollectionNameThree directly into export_job_123456, eliminating the numerical intermediaries.

Following restructuring, the directory structure appears as:

```
export_job_123456/
├── CollectionNameOne/
│   ├── page/
│   │   └── [PageXML files]
│   └── [other subdirectories and files]
├── CollectionNameTwo/
│   ├── page/
│   │   └── [PageXML files]
│   └── [other subdirectories and files]
├── CollectionNameThree/
│   ├── page/
│   │   └── [PageXML files]
│   └── [other subdirectories and files]
└── transkribus_id_mapping.csv
```

The CSV mapping file appears alongside the restructured collections, preserving the relationship between numerical identifiers and collection names.

## Usage

### Basic Execution

To process a Transkribus export, first extract the downloaded ZIP archive to a convenient location. Open a terminal or command prompt and execute the Python script:

```bash
python transkribus_restructure.py
```

The script prompts for the path to the extracted export directory. Provide the full path to the `export_job_[number]` directory:

```
Enter the path to your export_job folder: C:\Users\Username\Downloads\export_job_123456
```

The tool immediately begins scanning the directory structure, processing each collection in turn, and providing progress updates in the console. Upon completion, the restructured collections and mapping file are available in the specified directory.

### Alternative Invocation Methods

Researchers working frequently with Transkribus exports may prefer to modify the script to accept command-line arguments rather than prompting for input. Replace the input statement in the main execution block with:

```python
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transkribus_restructure.py <export_folder_path>")
        sys.exit(1)
    
    export_folder = sys.argv[1]
    if os.path.exists(export_folder):
        process_transkribus_export(export_folder)
    else:
        print(f"Error: Path not found: {export_folder}")
```

This modification enables direct execution with the path specified as an argument:

```bash
python transkribus_restructure.py "C:\Users\Username\Downloads\export_job_123456"
```

### Integration with Batch Processing

Researchers processing multiple Transkribus exports can integrate the restructuring tool into larger workflows. Create a batch script that iterates through multiple export directories:

```bash
#!/bin/bash
for dir in export_job_*/; do
    python transkribus_restructure.py "$dir"
done
```

This approach restructures all Transkribus exports in the current directory automatically, generating separate mapping files for each export.

## Processing Workflow

The restructuring tool follows a systematic workflow designed to ensure data integrity and comprehensive documentation. Upon invocation, the script first validates that the specified path exists and represents a directory. If validation succeeds, the tool begins scanning for subdirectories whose names consist entirely of numerical digits, as these represent Transkribus collection identifiers.

For each numerical directory discovered, the script examines its contents to identify user-named collection folders. The expected structure contains exactly one subdirectory per numerical directory, representing the single collection associated with that identifier. When this expected structure is encountered, the tool extracts both the numerical identifier and the user-assigned folder name, recording this correspondence in a list that will populate the final CSV file.

The tool then initiates the physical restructuring process. To avoid conflicts during the move operations, the script creates a temporary directory named `_temp_restructure` within the export folder. Each user-named collection folder is moved from its numerical parent directory into this temporary location. After the move completes, the now-empty numerical directory is removed from the filesystem. This two-stage process ensures that the original data remains intact even if an error occurs during restructuring.

Once all collections have been moved to the temporary directory, the script relocates them from the temporary location to the root of the export directory. This final move places all user-named folders at the appropriate level in the hierarchy. The temporary directory, now empty, is removed. Throughout this process, the tool monitors for naming conflicts. If two collections share identical user-assigned names, the tool appends a numerical suffix to subsequent instances, ensuring that all collections are preserved with unique directory names.

After completing the physical restructuring, the tool writes the mapping data to a CSV file named `transkribus_id_mapping.csv`. The file contains two columns labelled "Transkribus ID" and "Folder Name", with rows sorted numerically by identifier. This sorting facilitates lookup operations and allows researchers to quickly locate specific collections in the mapping.

The tool provides comprehensive error handling throughout the workflow. If a numerical directory contains no subdirectories, indicating an empty collection, the tool reports this anomaly but continues processing other collections. If a numerical directory contains multiple subdirectories, suggesting an unexpected structure, the tool reports this situation and preserves all discovered subdirectories in the temporary directory for manual review. These safeguards ensure that unusual export structures do not cause data loss or prevent processing of well-formed collections.

## Console Output

The restructuring tool provides detailed progress information throughout its execution, enabling researchers to monitor the process and identify any issues requiring attention. Initial output confirms the path being processed and the start of the scanning operation:

```
Scanning Transkribus export structure...
```

As the tool processes each collection, it displays the correspondence between numerical identifiers and user-assigned names:

```
Processing: 789012 -> CollectionNameOne
Processing: 789013 -> CollectionNameTwo
Processing: 789014 -> CollectionNameThree
```

If the tool encounters naming conflicts, it reports the resolution:

```
Processing: 789015 -> CollectionNameOne_1
```

This output indicates that a second collection named CollectionNameOne was discovered, and the tool assigned the name CollectionNameOne_1 to avoid overwriting the first instance.

Warning messages alert researchers to unusual structures:

```
Warning: Empty Transkribus ID folder: 789016
Warning: Multiple subfolders in 789017: ['FolderA', 'FolderB']
```

These warnings indicate situations requiring manual review. Empty folders may represent collections that were not properly exported or were deleted after export creation. Directories containing multiple subfolders suggest an unexpected export structure that may require special handling.

Upon completion, the tool reports the location of the mapping file and summary statistics:

```
Mapping saved to: C:\Users\Username\Downloads\export_job_123456\transkribus_id_mapping.csv

Restructuring complete. Processed 118 folders.
All folders now directly under: C:\Users\Username\Downloads\export_job_123456
```

These statistics allow researchers to verify that all expected collections were processed and that the restructuring completed successfully.

## CSV Mapping File

The generated CSV file serves as a permanent record of the relationship between Transkribus internal identifiers and user-assigned collection names. The file uses standard CSV formatting with comma-separated values and UTF-8 encoding to support collection names containing non-ASCII characters. The first row contains column headers "Transkribus ID" and "Folder Name", followed by data rows sorted numerically by identifier.

A representative mapping file appears as:

```csv
Transkribus ID,Folder Name
789012,CollectionNameOne
789013,CollectionNameTwo
789014,CollectionNameThree
789015,CollectionNameOne_1
```

This mapping proves valuable in several research scenarios. When correlating exported materials with collections visible in the Transkribus web interface, the numerical identifiers provide the necessary link. When troubleshooting export issues or verifying completeness, the mapping allows researchers to confirm that all expected collections were included in the export. When documenting research workflows, the mapping file serves as a record of which Transkribus collections contributed to subsequent analyses.

The CSV format facilitates integration with other tools and workflows. Researchers can open the file in spreadsheet applications for sorting and filtering, import it into database systems for joining with other metadata, or read it programmatically in analysis scripts that require knowledge of the collection identifiers.

## Troubleshooting

### Path not found error

**Problem**: The tool reports that the specified path does not exist.

**Solution**: Verify that you have extracted the Transkribus export ZIP file before running the restructuring tool. The script operates on the extracted directory, not on the compressed archive itself. Confirm that the path was typed correctly, including proper use of backslashes or forward slashes depending on your operating system. Windows paths use backslashes, Unix-like systems use forward slashes. If the path contains spaces, ensure it is enclosed in quotation marks when entered.

### Permission denied errors

**Problem**: The tool reports permission errors when attempting to move directories or create files.

**Solution**: Ensure that you have write permissions for the export directory and all its contents. On Windows systems, confirm that no files within the export directory are currently open in other applications, as this can prevent directory operations. On Unix-like systems, check the ownership and permissions of the directory using `ls -la` and modify as necessary using `chmod` or `chown`. Running the script with elevated privileges may be necessary in some environments, though this should not generally be required for directories in user-controlled locations.

### Empty numerical directories

**Problem**: The tool reports warnings about empty Transkribus ID folders.

**Solution**: Empty numerical directories indicate collections that were included in the export manifest but contain no actual data. This situation may arise if a collection was deleted in Transkribus after the export was initiated, if the collection never contained any documents, or if a partial export occurred due to an error. Review the empty directories manually and remove them if they serve no purpose. The restructuring tool preserves these directories and reports their presence but does not automatically delete them to avoid unintended data loss.

### Multiple subfolders in numerical directory

**Problem**: The tool reports that a numerical directory contains multiple subfolders.

**Solution**: The expected Transkribus export structure places exactly one user-named folder within each numerical directory. Multiple subfolders suggest either an unusual export configuration or manual modification of the export structure after extraction. Examine the affected numerical directory manually to determine which subfolder represents the actual collection. The tool does not automatically restructure directories with multiple subfolders, as it cannot determine which subfolder should be promoted to the root level. Manually relocate the appropriate subfolder, then run the restructuring tool again.

### Naming conflicts not handled as expected

**Problem**: Collections with identical names do not receive numerical suffixes as described.

**Solution**: The tool appends numerical suffixes only when moving collections from the temporary directory to the export root. If multiple collections share the same name, subsequent instances receive suffixes like _1, _2, and so forth. If suffixes are not appearing, verify that the collections actually have identical names including capitalisation and spacing. The tool performs case-sensitive comparison, so "Collection Name" and "collection name" are treated as different names. If suffixes appear unexpected, check whether you have run the restructuring tool multiple times on the same export, as each execution may add additional suffixes.

### CSV file encoding problems

**Problem**: The mapping CSV file displays garbled characters when opened in certain applications.

**Solution**: The tool writes CSV files using UTF-8 encoding to support collection names containing characters from various writing systems. Some applications, particularly older versions of Microsoft Excel, do not automatically detect UTF-8 encoding. When opening the file in Excel, use the "Get Data" or "Import" function rather than double-clicking the file, and explicitly specify UTF-8 as the encoding. Alternatively, open the file in a text editor that supports UTF-8, such as Notepad++ or Visual Studio Code, to verify that the data is correctly encoded.

### Restructuring appears to complete but folders remain nested

**Problem**: After running the tool, the numerical directories still exist with collections nested within them.

**Solution**: This situation may indicate that an error occurred during the restructuring process but was not properly reported. Check the console output for any error messages that may have been overlooked. Verify that the specified path points to the correct export directory, not to a subdirectory within it. The tool expects to find numerical directories as immediate children of the specified path. If you pointed to a numerical directory rather than to the export_job directory, the tool will not find collections to restructure. Run the tool again with the correct path to the export_job directory.

## Best Practices

When working with the Transkribus export restructuring tool, several practices enhance reliability and facilitate integration with broader research workflows. Before restructuring an export, create a backup copy of the extracted export directory. The restructuring process modifies the directory structure in place, and a backup enables recovery if unexpected issues arise. Storage space permitting, retain the original ZIP archive downloaded from Transkribus as an additional safeguard.

Process Transkribus exports promptly after extraction to avoid confusion about which exports have been restructured and which retain the original nested structure. If multiple exports are being processed, establish a clear naming convention for export directories that indicates their status. A simple approach appends "_restructured" to the directory name after processing, preventing accidental reprocessing.

Review the console output carefully during restructuring, particularly the warning messages about empty directories and multiple subfolders. These warnings often indicate export issues that may require investigation. Document any unusual structures encountered and their resolution, as this information assists with troubleshooting similar issues in future exports.

Examine the generated CSV mapping file after restructuring to verify that all expected collections appear and that numerical identifiers are correctly associated with collection names. This verification step catches errors early and ensures that the mapping file can serve as a reliable reference for subsequent work. If collections are missing or incorrectly mapped, investigate the original export structure before proceeding with analysis.

Integrate the mapping file into your research documentation and data management practices. Store it alongside the restructured collections rather than in a separate location, ensuring that the relationship between identifiers and names remains accessible. If you transfer collections to different storage systems or share them with collaborators, include the mapping file to preserve the connection to Transkribus identifiers.

When working with large exports containing dozens or hundreds of collections, consider processing them in stages rather than restructuring all collections simultaneously. This approach facilitates monitoring and troubleshooting, particularly if specific collections are known to present structural issues. The tool processes collections independently, allowing selective restructuring of subsets if needed.

## Integration with Research Workflows

The restructuring tool forms part of a larger workflow for processing Transkribus exports and preparing materials for analysis. A typical workflow begins with exporting collections from Transkribus, selecting the appropriate export format and options based on subsequent analysis requirements. After downloading the export archive, extract it to a working directory with sufficient storage space for both the compressed and extracted forms.

Execute the restructuring tool on the extracted export to flatten the directory hierarchy and generate the identifier mapping. Review the console output and verify that restructuring completed successfully. Examine the mapping CSV file to confirm that all expected collections appear and that no naming conflicts require resolution. At this stage, the export structure is ready for integration with analysis tools and scripts.

Subsequent workflow steps depend on research objectives. Researchers working with PageXML files may use tools like the PageXML Geographical Location Mapper to extract and visualise place mentions from the restructured collections. The flattened directory structure simplifies path handling in such tools, as collections are directly accessible without navigating through numerical directories. Researchers conducting text analysis may iterate through the restructured collections to extract transcription data, build corpora, or perform named entity recognition.

The identifier mapping file supports quality control and documentation throughout these processes. When correlating analysis results with specific Transkribus collections, the mapping enables lookup of the original collection identifiers. When documenting research methods and data provenance, the mapping provides a clear record of which Transkribus collections contributed to the analysis. When sharing processed data with collaborators, the mapping allows them to locate the original collections in Transkribus if they require access to source materials or metadata.

Researchers maintaining local databases of collection metadata can import the mapping CSV file to establish relationships between their database records and Transkribus collections. This integration enables queries that span local and Transkribus-based information, supporting comprehensive collection management and facilitating discovery of relevant materials.

## Extending the Tool

The restructuring tool can be extended to support additional requirements that may arise in particular research contexts. Common extensions include adding support for custom mapping file formats, implementing filtering to restructure only selected collections, incorporating metadata extraction from PageXML files during restructuring, and generating additional documentation about collection structure and contents.

### Custom Mapping File Formats

Researchers requiring mapping data in formats other than CSV can modify the mapping generation section of the script. To generate JSON output alongside the CSV file:

```python
import json

# After CSV writing section
json_path = export_path / 'transkribus_id_mapping.json'
json_data = {item[0]: item[1] for item in mapping_data}
with open(json_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(json_data, jsonfile, ensure_ascii=False, indent=2)
```

This extension creates a JSON file where Transkribus identifiers serve as keys and collection names as values, facilitating programmatic access in environments where JSON parsing is more convenient than CSV processing.

### Selective Restructuring

To restructure only collections matching specific criteria, add filtering logic to the main processing loop:

```python
# Define collections to process
target_collections = ['CollectionNameOne', 'CollectionNameTwo']

for item in export_path.iterdir():
    if item.is_dir() and item.name.isdigit():
        transkribus_id = item.name
        subfolders = [f for f in item.iterdir() if f.is_dir()]
        
        if len(subfolders) == 1:
            human_folder = subfolders[0]
            human_name = human_folder.name
            
            # Filter based on collection name
            if human_name not in target_collections:
                print(f"Skipping: {transkribus_id} -> {human_name}")
                continue
            
            # Process as normal
```

This modification allows researchers to restructure specific collections without affecting others, useful when working with partial exports or when only certain collections require processing.

### Metadata Extraction

Researchers can extend the tool to extract and aggregate metadata from PageXML files during restructuring:

```python
def extract_metadata(collection_path):
    metadata = {
        'page_count': 0,
        'word_count': 0,
        'has_coordinates': False
    }
    
    page_dir = collection_path / 'page'
    if page_dir.exists():
        xml_files = list(page_dir.glob('*.xml'))
        metadata['page_count'] = len(xml_files)
        # Additional metadata extraction logic
    
    return metadata
```

Integrating this function into the restructuring workflow generates a metadata summary alongside the identifier mapping, providing immediate insight into collection contents without requiring separate analysis passes.

## Limitations

The restructuring tool operates within several constraints that researchers should understand. The tool assumes that Transkribus exports follow the standard structure with numerical directories containing single user-named subdirectories. Exports with non-standard structures may require manual intervention or script modification. The tool does not validate that the contents of user-named directories conform to expected Transkribus export formats; it restructures directories regardless of their contents.

Naming conflict resolution appends numerical suffixes without attempting to preserve semantic distinctions between collections. If multiple collections legitimately share the same name, researchers must manually differentiate them after restructuring based on their contents or Transkribus identifiers. The tool provides no mechanism for reverting the restructuring operation; once executed, the original nested structure cannot be automatically restored without access to the original ZIP archive.

The mapping file documents only the final relationship between identifiers and folder names after conflict resolution. If a collection was renamed due to conflicts, the mapping reflects the modified name rather than the original user-assigned name. Researchers requiring a record of name modifications must parse the console output or extend the tool to log such changes separately.

These limitations reflect the tool's design as a focused utility for a specific restructuring task. The tool transforms directory hierarchies efficiently and documents identifier relationships comprehensively, leaving broader collection management and analysis tasks to specialised tools and workflows.

## Related Tools and Resources

The Transkribus export restructuring tool complements various other tools and resources in digital humanities and historical research workflows. Transkribus itself provides the platform for transcription and export, whilst the restructuring tool prepares exported materials for subsequent analysis. Tools like the PageXML Geographical Location Mapper operate on the restructured collections, benefiting from the simplified directory structure.

For researchers working with large numbers of exports across multiple projects, collection management systems and digital repository platforms provide mechanisms for organizing and accessing restructured materials. Integration with version control systems such as Git enables tracking of changes to collection structures and facilitates collaboration on shared collections. Metadata management tools can incorporate the generated CSV mapping files to establish comprehensive collection catalogues.

Documentation generators can process restructured exports to create human-readable collection inventories and finding aids. Text analysis platforms and named entity recognition tools benefit from the predictable directory structure that restructuring provides, enabling batch processing of PageXML transcriptions without complex path manipulation. Visualisation tools for spatial and temporal analysis can incorporate the identifier mappings to link analytical results back to source collections.

## Licence

This project is licensed under the MIT Licence, permitting free use, modification, and distribution in academic and commercial contexts.

## Contact

- Email: c.a.romein@utwente.nl

## Acknowledgements

This Transkribus Export Restructuring Tool was developed within the context of the [HAICu project](https://haicu.science) on the Resoluties van de Staten van Overijssel (Resolutions of the States of Overijssel), funded by the Dutch Research Council/Nederlandse Organisatie voor Wetenschappelijk Onderzoek/Nationale Wetenschapsagenda [NWA.1518.22.105].

Development was assisted by Claude (Anthropic) for code implementation and documentation.

## Version History

**Version 1.0** (2025): Initial release with automated directory restructuring, CSV mapping file generation, naming conflict resolution, comprehensive error handling and reporting, and support for standard Transkribus export structures.