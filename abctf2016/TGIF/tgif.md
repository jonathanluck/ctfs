#TGIF

### Programming

We get a file containing a list of [dates](https://raw.githubusercontent.com/jonathanluck/ctfs/master/abctf2016/TGIF/date.txt), and our goal is to add a year to each date, then check if it is a Friday. We need to get the total number of Fridays.

To start we do a little bit of find and replace to format the dates as an array of strings:

`['September 11, 2003', 'November 2, 2009', 'April 6, 2004', 'May 24, 2007', 'December 25, 2005', ...]`

We can just directly paste that into our browser console (js will handle leap years for us, so we will use js). It will be saved into a variable called `dates`

Next we need to create a counter to hold the number of Fridays. It will be stored in `count`.
 
Now we need to loop over all the dates in the array, make a new Date object for each one, increment the year, then check if it is a Friday. We can do that with this code:

```javascript
dates.forEach(function(e){
    d = new Date(e);
    y = d.getFullYear() + 1;
    d.setFullYear(y);
    if(d.getDay() == 5){
        count++;
    }
});
```

`d = new Date(e)` creates a new [Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date) object that we can manipulate.

`y = d.getFullYear() + 1` and `d.setFullYear(y)` increments the year

`d.getDay() == 5` checks if the new date is a Friday.

Putting it all together, `count` ends up being 194.

Flag: `ABCTF{194}`
