# Cookie

We start by getting a page indicating we are not an admin user. 

Looking at the page's cookie (as the title of the problem hints at) we find the entry `coookie=e2FkbWluOmZhbHNlfQ%3D%3D`. `%3D` translates to `=`, which probably means that the cookie is base64 encoded.

Running `atob("e2FkbWluOmZhbHNlfQ==")` from a browser js console nets us `{admin:false}`. So it looks like the page knows who is admin based on this cookie. Lets break it.

* First, we want to indicate we are admin. This is looks as simple as changing `{admin:false}` to `{admin:true}`. 
* Next we need to make the cookie "look" right. To do this we will follow the same format as the original cookie: `coookie=[base64 encoded key/value pair]`. To obtain the b64 value, we can run `btoa("{admin:true}")`. 
* Lastly we need to put it all together and set the cookie. This can be done in most browsers with `document.cookie=[what you want to set the cookie to]`. Combing all the above elements, we get `document.cookie = "coookie"+btoa("{admin:true}")`

![alt text](https://raw.githubusercontent.com/jonathanluck/ctfs/master/abctf2016/Chocolate/ss%20%282016-07-22%20at%2011.16.46%29.png "this")

We then refresh the page to get the flag

![alt text](https://raw.githubusercontent.com/jonathanluck/ctfs/master/abctf2016/Chocolate/ss%20%282016-07-22%20at%2011.17.43%29.png "this")

Flag: `ABCTF{don't_trust_the3_coooki3}`