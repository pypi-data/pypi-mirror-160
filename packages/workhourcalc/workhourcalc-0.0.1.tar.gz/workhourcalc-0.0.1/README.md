# Python Package - workhourcalc

develop a packages that gets the input opening and closing time of restaurants in millisecond and writes the working hours intervals in human readable format

### Install the package
1. First copy workhourcalc-0.0.1.tar.gz package file from the dist folder.
2. paste in your current project location. then install using below pip command.

###`pip install workhourcalc`

### Use package method to calculate work hours
```
from calc_work_hours.main import calculate_working_hours`

output = calculate_working_hours("/file/path/to/input_json file")
print(output)
```
### Package Dependencies
1. You need to use valid json input file for the package.

Ex:
<pre>{
  "monday": [],
  "tuesday": [
    {
      "type": "open",
      "value": 36000
    },{
      "type": "close",
      "value": 3600
    }
  ],
  "wednesday": [],
  "thursday": [
    {
      "type": "open",
      "value": 36000
    },{
      "type": "close",
      "value": 3600
    }
  ],
  "friday": [],
  "saturday": [],
  "sunday": [
    {
      "type": "open",
      "value": 3600
    },{
      "type": "close",
      "value": 3600
    }
  ]
}
}</pre>

2. When you set file path make sure to set valid file path.

Ex:
`C:\Users\HP\Downloads\Dashmote-Home-Assignment for Python Engineer\input.json`

# Python Project - calc_work_hours

### Setup the project

1. install the tool to create environment
   ####`pip install virtualenv`
2. create virtual environment
    ####`virtualenv environment_name`
3. activate a virtual environment
    ####`source virtualenv_name/bin/activate`
4. install the requirement.txt file
    ####`pip install -r requirement.txt`

### Run the project-application
can execute below function in main.py file with json input file path
###```def calculate_working_hours(json_file_path)```

### Project Structure
```
calc_work_hours
    |
    |----calc_work_hours
    |           |-- __init__.py
    |           |-- main.py           *main function defined in here
    |           |-- controller.py     *work hour calculate logics   
    |           |-- json_utils.py     *json file related
    |           |-- schema.py         *json schemas
    |           |__ utils.py          *other util funcs. 
    | 
    |___tests    
          |-- __init__.py
          |-- test_main.py
          |-- test_controller.py    
          |__ test_utils.py    
```
