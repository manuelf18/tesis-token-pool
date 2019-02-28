    /**
        * returns a substring of [value] after [match] is found
        * @param {string} value The string which we want the substring of
        * @param {string} match
        * @param {number} position  The index at which to begin searching the String object. If omitted, search starts at the beginning of the string.
    */

const substringAfter = (value, match, position) => {
    if(value.indexOf(match) === -1)
        return "";
    return value.substring(value.indexOf(match, position) + match.length);
}