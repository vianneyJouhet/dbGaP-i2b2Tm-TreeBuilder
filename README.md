# dbGaP-i2b2Tm-TreeBuilder
Builds i2b2 tranSMART ontology from an dbGaP study

This python script queries dbGaP projects web pages base on a phs (study id) in order to retrieve contextual information for dbGaP phv (variables id). 

Using these information it builds a set of i2b2 ontology paths for each phv. These informations are stored in a file (leafFilePath). These file is then used to create a new mappig file for the i2b2/tranSMART etl pipeline (based on a pre-existing one)

## Usage


### Pre requisit
python 2 (should work with python 3)

### Clone the repository
```bash
git clone https://github.com/vianneyJouhet/dbGaP-i2b2Tm-TreeBuilder.git
```
### Copy and adapt the properties.json file
Copy ```properties.json``` from template to the root of the project

 *  **study_id** ==> dgGap study id (phs that includes version and p) 
 *  **current_object_id** ==> dbGap object id (number within the phs)
 *  **retrievePaths** ==> do you want yo retrieve path from dbGap (can be set to "N" in order to skip this part)
 *  **buildMappingFile** ==> do you want to build a mapping file (needs sourceMappingFile and targetMappingFile to be set)
 *  **leafFilePath**  ==> Target file for tree building (will replace file if exists)
 *  **sourceMappingFile** ==> Pre-existing Mapping file as defiend in i2b2 TranSMART ETL)
 *  **targetMappingFile** ==> Mapping File that will be created



### Run the main script
```bash
python main.py
```
