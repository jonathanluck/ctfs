#L33t H4xx0r  (Web 6)

### Web exploitation

We start off by getting a site with a single password field and a taunting message. Checking the HTML of the page, we get a comment indicating the source is in /source.txt. Shown below:

```php
<?php
	$FLAGWEB6 = (file_get_contents("flag.txt"));
	$PASSWORD =  (file_get_contents("flag.txt")); //haha


	if(isset($_GET['password'])){
	
	if(strcmp($PASSWORD, $_GET['password']) == 0){
			$success = true;
		}
		else{
			$success = false;
		}

	}
	else {
		$success = false;
	}
	
	

?>
```

<b> Note the line:</b> `strcmp($PASSWORD, $_GET['password']) == 0`

This line essentially says: compare our secret password to whatever the user passed in in the password field of the GET request, and check if they are the same.

However, because they used a `==` comparison instead of a `===` comparison, this is exploitable. [When `strcmp` receives an array as one of its parameters, it will return `NULL`](http://php.net/manual/en/function.strcmp.php#113364). Using the `===`, `NULL===0` would be false. However using the `==` operator, `NULL==0` actually evaluates to true. Thus, we can bypass this `strcmp` check by passing in an array as the password parameter.

Normal GET request with password "abc":
![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/abctf2016/Web%206/clip%20%282016-07-19%20at%2007.50.23%29.png)

We can pass in an array by changing `?password=abc` to `?password[]=abc` then resubmitting the GET request. Doing so gets us the flag:

![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/abctf2016/Web%206/clip%20%282016-07-19%20at%2007.50.53%29.png)

Flag: ` abctf{always_know_whats_going_on} `