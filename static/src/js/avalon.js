var avalon = {};

var is = {
    types : ["Array", "Boolean", "Date", "Number", "Object", "RegExp", "String", "Window", "HTMLDocument", "Function"]
}

for(var i = 0, c; c = is.types[i ++ ]; )
{
    is[c] = (function(type)
    {
        return function(obj)
        {
            return Object.prototype.toString.call(obj) == "[object " + type + "]";
        }
    }
    )(c);
}

$.extend({
    is: is,
})


Module = function(name, func){
    function prepare(arg){
        if (arg.length != 2){
            throw('require two parameters!');
        }

        if ($.is.String(name)){
            if (name.length < 1){
                throw('arg <name> is required!');
            }
        }

        if (!$.is.Function(func)){
            throw('arg <func> is not a function!');
        }
    }

    prepare(arguments);

    if (avalon.hasOwnProperty(name)){
        throw(name + ' has been declared!');
    }

    that = {'exports': {}}; 
    func.apply(that);
    avalon[name] = that;
}
