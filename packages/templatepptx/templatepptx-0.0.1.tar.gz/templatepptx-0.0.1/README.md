# PowerPoint Template Engine

Use PowerPoint templates to generate PowerPoint files on the fly using "magic words". Magic words are specified by using the `$` sign symbol. This keyword becomes a special reserved symbol. If this magic symbol is not suitable, it can be changed within the script. You can specify magic words in PowerPoint templates by wrapping the word like `$this$`. The data is opulated by using a "context" object. A context object is a dictionary which contains the keywords and thier values that are used to populate the powerpoint. Additionally, tables can be populated with an unlmited number of related data by specifying a list of dictionaries in your context. 

There are two methods to run this tool:

COMMAND LINE & CONFIG FILE: The tool expects a config file which contains the input pptx template file with magic words and an output pptx file. Additionally, a context file must be specified. Example: `main.py --config "path\\to\\config\\file.json" --context "path\\to\\context_file.json"`

CALLED FROM ANOTHER PYTHON FILE: You can import the library and then call `parse_template_ppt(ppt, context, output_path)`



To prepare to run the script, download or clone the repo to your local machine. Then use the command line to install the requirements in your desired Python environment using pip: `pip install -r /path/to/requirements.txt`





