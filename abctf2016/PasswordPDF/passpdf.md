# PasswordPDF

### Forensics

So we get a PDF that is password protected. The hint essentially says to guess the password. This problem is pretty straight forward.

To start, we need a tool that will guess the password for us. I just used [this one](http://www.cyberciti.biz/tips/linux-howto-crack-recover-pdf-file-password.html).

Next we need to figure out what to guess for the password. We have two main options: brute force or dictionary attack. 

* Brute forcing is guessing every single letter/number/symbol combination (can be limited to subsets of those) of a certain length. Brute forcing can be very slow, but it is guaranteed to find the password if you choose the correct keyspace/length combination.

* Dictionary attacks involve guessing using a word list of some sort.  Dictionary attacks are much faster due to a smaller number of guesses, but the actually password is never guaranteed to be in the dictionary you use.

I personally prefer to throw a dictionary at these problems first, then brute force if that fails.

Because I have a [Kali Linux](https://www.kali.org/) VM, I used that. Kali has a built in [wordlist](http://www.wirelesshack.org/word-list-dictionaries-built-into-kali.html) (aka a dictionary) that we can use.

So now we have a cracker, a dictionary, and a PDF to crack. Putting it all together we get the command: `pdfcrack -f mypassword.pdf -w /usr/share/wordlists/rockyou.txt`

Running that gets us the password `elephant`

![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/abctf2016/PasswordPDF/clip%20%282016-07-19%20at%2007.23.55%29.jpg)

Opening the PDF and entering that password gets us a document that says the password is censored. Oh no....

Selecting all (CTRL+A) shows us that there is actually some hidden text underneath the censoring box. That hidden text is the flag: `ABCTF{Damn_h4x0rz_always_bypassing_my_PDFs}`

![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/abctf2016/PasswordPDF/clip%20%282016-07-20%20at%2006.17.36%29.png)
