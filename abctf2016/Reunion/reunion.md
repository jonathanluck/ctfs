# Reunion

### Web exploitation

We get a page where we can enter an ID number and we get back a dog's name, breed, and color. The problem title hints that we should be using the union command.

##### Number of columns
First we need to determine the number of selected columns.  To do this, we repeatedly enter `1 order by n` where `n` is an number we increment each time. We repeat this until we get no results (i.e. we enter `1 order by 2`, `1 order by 3`, ... until we get 0 results). When entering `1 order by 5`, we get no results, indicating that we have 4 columns (ID, name, breed, and color). We can verify this by noting that `1 union all select 1,2,3,4` gets us a result, but `1 union all select 1,2,3,4,5` does not.


##### Version, tables, and columns

We can then extract more information about the SQL database. Entering `1 union all select 1, @@version,3,4` nets us `5.5.49-0ubuntu0.14.04.1`. The version number is important in choosing the injection string for extracting table/column names. 

To enumerate table names we can use `1 union all select 1,table_name,3,4 from information_schema.tables`. Doing so gets us an interesting table name:

![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/abctf2016/Reunion/ss%20%282016-07-22%20at%2011.09.35%29.png)

We perform a similar enumeration for column names with `5 union all select 1,column_name,3,4 from information_schema.columns`

An interesting column name appears at the end:

![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/abctf2016/Reunion/ss%20%282016-07-22%20at%2011.10.02%29.png)

##### Getting the flag. 

It is a reasonable assumption that the flag is in `f0und_m3` and `w0w_y0u_f0und_m3`. 

We can extract information from that table/column combo with `1 union all select 1,f0und_m3,3,4 from w0w_y0u_f0und_m3`
![](https://raw.githubusercontent.com/jonathanluck/ctfs/master/abctf2016/Reunion/clip%20%282016-07-22%20at%2011.10.45%29.png)
With that we obtain the flag: `abctf{uni0n_1s_4_gr34t_c0mm4nd}`