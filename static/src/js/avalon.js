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
            throw('require two parameters <name> and <func>!');
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

    if (avalon.hasOwnProperty(name)){
        return;
    }

    prepare(arguments);

    that = {'exports': {}}; 
    func.apply(that);
    avalon[name] = that.exports;
    if (that.run && $.is.Function(that.run)){
        that.run();
    }
}
