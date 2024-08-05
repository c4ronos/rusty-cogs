# Regular Expressions List
---
`\`     // the escape character - used to find an instance of a metacharacter like a period, brackets, etc.\
`.`     // match any character except newline\
`x`     // match any instance of x\
`[^x]`   // match any character except x\
`[x]`    // match any instance of x in the bracketed range - [abxyz] will match any instance of a, b, x, y, or z\
`|`     // an OR operator - [x|y] will match an instance of x or y\
`()`    // used to group sequences of characters or matches\
`{}`    // used to define numeric quantifiers\
`{x}`    // match must occur exactly x times\
`{x,}`     // match must occur at least x times\
`{x,y}`   // match must occur at least x times, but no more than y times\
`?`     // preceding match is optional or one only, same as {0,1}\
`*`     // find 0 or more of preceding match, same as {0,}\
`+`     // find 1 or more of preceding match, same as {1,}\
`^`     // match the beginning of the line\
`$`     // match the end of a line\
<br/><br/>
`[:alpha:]`   // Represents an alphabetic character. Use [:alpha:]+ to find one of them.\
`[:digit:]`   // Represents a decimal digit. Use [:digit:]+ to find one of them.\
`[:alnum:]`   // Represents an alphanumeric character ([:alpha:] and [:digit:]).\
`[:space:]`   // Represents a space character (but not other whitespace characters).\
`[:print:]`   // Represents a printable character.\
`[:cntrl:]`   // Represents a nonprinting character.\
`[:lower:]`   // Represents a lowercase character if Match case is selected in Options.\
`[:upper:]`   // Represents an uppercase character if Match case is selected in Options.\
<br/><br/>
`\d`    // matches a digit, same as [0-9]\
`\D`    // matches a non-digit, same as [^0-9]\
`\s`    // matches a whitespace character (space, tab, newline, etc.)\
`\S`    // matches a non-whitespace character\
`\w`    // matches a word character\
`\W`    // matches a non-word character\
`\b`    // matches a word-boundary (NOTE: within a class[], matches a backspace)\
`\B`    // matches a non-word-boundary\
<br/><br/>
`(?i)`   // makes regex case-insensitive\

<br/><br/>
# Resources
---
https://regex101.com/           // test all regex here\
https://net.tutsplus.com/tutorials/other/8-regular-expressions-you-should-know/     // regex examples\
https://regexlib.com\

<br/><br/>
# Examples
---
**// Match Everything**\
`.*`
<br/><br/>
**// Alphanumericals**\
`[A-Za-z0-9]?.*`\
matches text consisting of letters and/or numbers
<br/><br/>
**// Non-alphanumericals**\
`[^A-Za-z0-9]`\
matches text NOT consisting of letters and/or numbers
<br/><br/>
**// Big Text**\
`^#{1,3}\s.*`\
matches text starting with # or ## or ###
<br/><br/>
**// Blank line**\
`^$`
<br/><br/>
**// Positive integers**\
`^[1-9]+[0-9]*$`
<br/><br/>
**// Positive decimal values**\
`(^\d*\.?\d*[0-9]+\d*$)|(^[0-9]+\d*\.\d*$)`
<br/><br/>
**// Invite Links 1**\
`(?i)(https?)?(://)?(discord\.gg/)[A-Za-z0-9]?.*`\
matches discord.gg/ invite links
<br/><br/>
**// Invite Links 2**\
`(?i)(https?)?(://)?(discord\.com/)(invite/)[A-Za-z0-9]?.*`\
matches discord.com/invite/ invite links
<br/><br/>
**// Percentage (2 decimal places)**\
`^-?[0-9]{0,2}(\.[0-9]{1,2})?$|^-?(100)(\.[0]{1,2})?$`
<br/><br/>
**// State abbreviation**\
`[A-Z][A-Z]`
<br/><br/>
**// City, State abbreviation**\
`.*, [A-Z][A-Z]`                 //Houston, TX
<br/><br/>
**// Phone Numbers**\
`(^\+[0-9]{2}|^\+[0-9]{2}\(0\)|^\(\+[0-9]{2}\)\(0\)|^00[0-9]{2}|^0)([0-9]{9}$|[0-9\-\s]{10}$)`
<br/><br/>
**// Zip Code**\
`[0-9]\{5\}(-[0-9]\{4\})?`            //84094 or 84094-1234
<br/><br/>
**// Social security number, such as: ###-##-####**\
`[0-9]\{3\}-[0-9]\{2\}-[0-9]\{4\}`
<br/><br/>
**// Dollar amounts, specified with a leading $ symbol**\
`\$[0-9]*.[0-9][0-9]`
<br/><br/>
**// DATE**\
`[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}`                 //2003-08-06\
`[A-Z][a-z][a-z] [0-9][0-9]*, [0-9]\{4\}`               //Jan 3, 2003\
`^(\d{1,2})\/(\d{1,2})\/(\d{2}|(19|20)\d{2})$`            //DD/MM/YY or DD/MM/YYYY or MM/DD/YY or MM/DD/YYYY
<br/><br/>
**// URL\
`^http(s)?:\/\/((\d+\.\d+\.\d+\.\d+)|(([\w-]+\.)+([a-z,A-Z][\w-]*)))(:[1-9][0-9]*)?(\/([\w-.\/:%+@&=]+[\w- .\/?:%+@&=]*)?)?(#(.*))?$/i`
<br/><br/>
// Credit Cards**\
`^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6011[0-9]{12}|622((12[6-9]|1[3-9][0-9])|([2-8][0-9][0-9])|(9(([0-1][0-9])|(2[0-5]))))[0-9]{10}|64[4-9][0-9]{13}|65[0-9]{14}|3(?:0[0-5]|[68][0-9])[0-9]{11}|3[47][0-9]{13})*$`
<br/><br/>
**// Email address**\
`^[\\w\\-]+(\\.[\\w\\-]+)*@([A-Za-z0-9-]+\\.)+[A-Za-z]{2,4}$`\
`^[\w-]+(\.[\w-]+)*@([a-z0-9-]+(\.[a-z0-9-]+)*?\.[a-z]{2,6}|(\d{1,3}\.){3}\d{1,3})(:\d{4})?$`\
`^([\w\.*\-*]+@([\w]\.*\-*)+[a-zA-Z]{2,9}(\s*;\s*[\w\.*\-*]+@([\w]\.*\-*)+[a-zA-Z]{2,9})*)$`   //List of semi-colon seperated email addresses\
`^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})*$`
<br/><br/>
**// IP Address**\
`^((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))*$`
