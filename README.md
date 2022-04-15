The base format is designed as follows
```
{
    "role-type": {
        "intro": "intro sentence",
        "role-keywords-demo": "sentence",
        "end": "ending sentence"
    }
}
```
**Note** the keys `intro` and `end` are required and are automatically picked. 
At the moment you can't disable it. 
*covlet-gen* will automatically find them and insert them into the intro and end of the cover letter.

Since you might be confused, this example should help illustrate the format you should follow.
```
{
    "front-end": {
        "intro": "I like the front-end",
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
This will allow you to specify the *company name* and the *job name* as a cli arg. If you have specified a line with  
the keyword `@company` and/or `@job`, then they will be replaced in the output file.  
Example:
```
{
    "scripting": ["I am applying to @company for the job @job and this is my application"]
}
```
you can then replace the `@company` and `@job` in this via the following cli args:
```
$ python main.py --keyword scripting --company test-company --job test-job
                        ^ this is just to select the scripting template
```
Your output string will then look like this.  
I am applying to *test-company* for the job *test-job* and this is my application