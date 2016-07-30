# JS PLS
###Reverse Engineering

Opening the file, we find a huge chunk of base64 encoded stuff that gets converted into a string and `eval`ed.

Calling `atob` on this, we get some js that starts with 

`process.stdin.resume();process.stdin.setEncoding('utf8');console.log("Give me a flag");process.stdin.on('data',(t)=>{t=t.trim();if(t.length===+[[+!+[]]...`

followed by a bunch of random array junk.

At this point, I just opened this in notepad++ because it lets me see matching parentheses and brackets.

After that, I plugged sections of random junk into the JS console on my browser to clean up the code.

For example,

`+[[+!+[]]+[!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]+!+[]]]`

is actually just `19`.

Going through the whole file isn't too bad, and in the end you get a pretty straighforward reversing problem. 
