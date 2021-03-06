# covlet-gen
A tool to generate more specialized cover letters, easily.  
## background
I'm a software engineer, a full stack engineer to be exact, and as such there are around 4 types of jobs I apply to.  
1. Software Engineer
2. Full stack engineer
3. Frontend engineer
4. Backend engineer

For each job, there is a different set of achievements they are looking for in a candidate, like:
- Product building
- Performance
- Open source work
- Remote
- Sideprojects
- Initiative

You get the idea. As such my cover letters need to be changed rather frequently, and I don't do that, I just reuse them  
knowing that this probably could be much better. Sometimes, I just dont bother applying, and when I do it takes so much  
more effort. So I built this.
Best thing, 1 command line command, with multiple arguments, and it generates a cover letter that I can copy to clipboard,  
or just generate a pdf from.
## Requirements
- python 3.10.2
This needs a few tools, specifically for pdf file generation:
- fpdf==1.7.2 # pdf generation
- pyperclip==1.8.2 # copy to clipboard library (just makes multiplatform handling hassle free)


**OR**  
just do `pip install -r requirements.txt`
## Usage and Description
The base format is designed as follows
```
{
    "role-type": {
        "intro": "intro sentence",
        "desc": "description sentence about the role"
        "role-keywords-demo": "sentence",
        "end": "ending sentence"
    }
}
```
**Note** the keys `intro`, `desc` and `end` are required and are automatically picked. 
At the moment you can't disable it. 
*covlet-gen* will automatically find them and insert them into the intro, description (where you introduce yourself  
and your love for that particular type of role) and end of the cover letter.

Since you might be confused, this example should help illustrate the format you should follow.
```
{
    "front-end": {
        "intro": "I like the front-end",
        "desc": "I like the front-end because I like the UIs",
        "product": "I built this amazing product that does X",
        "end": "I hope you know I like the front-end"
    }
}
```
This is just a layer of abstraction to make sentence picking easier. There is no automatic  
detection. You as the user can choose to use this and use the `--role` and `--keyword` option  
to follow this. It is available to you. Otherwise, you can just mention a `--keyword` and it will  
treat it as follows. (you will need to be following the correct format)  
```
$ python main.py --keyword product
```
This expects the following template
```
{
    "intro": "I am a non nesting required intro",
    "product": "I made some X product that did Y",
    "end": "I am a non nesting required end"
}
```
So basically no nesting.

## job and company name replacements
Json by default cant use or handle any variable names. So covlet-gen uses its own special characters for this.  
This will allow you to specify the *company name* and the *position name* as a cli arg. If you have specified a line with  
the keyword `@company` and/or `@position`, then they will be replaced in the output file.  
Example:
```
{
    "scripting": ["I am applying to @company for the position @position and this is my application"]
}
```
you can then replace the `@company` and `@position` in this via the following cli args:
```
$ python main.py --keyword scripting --company test-company --position test-position
                        ^ this is just to select the scripting template
```
Your output string will then look like this.  
I am applying to *test-company* for the position *test-position* and this is my application

## Output - Copy to clipboard and Export as Pdf
Lastly, the one I really like. You can choose to copy the generated cover letter to your clipboard,  
or output to pdf. The files will be output to the output folder  
**Required:** The flag `--out`, followed by the cover letter file name you want like `cover-letter-test`.  
This will generate a file called **cover-letter-test.pdf** in the project output folder.