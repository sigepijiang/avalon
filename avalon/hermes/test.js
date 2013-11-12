// node test.js


// js source code 'new'
// Function('new', function(){
//     var that = Object.create(this.prototype);
//     var other = this.apply(that, arguments);
//     return (typeof other === 'object' && other) || that;
// })


Class = function(){
}

Class.prototype.test = {}

class1 = new Class()
class2 = new Class()

// print object
console.log(typeof class1)
// print object
console.log(typeof Class)
// print object
console.log(typeof Object)

// print true
console.log(class1.test === class2.test)
class1.test['a'] = 2
// print {a : 2}
console.log(class2.test)

console.log(Class.prototype)


// call && apply
Class2 = function(){
    console.log('in Class2')
    // print {a : 2}
    console.log(this.prototype.test)
    // nice arguments! 
    console.log(arguments)
    return {}
}

// print {}
console.log(Class2.call(Class))

var global_this = undefined
Class = function(){
    this.test = {}
    console.log(this.prototype)
    console.log(this)
    global_this = this
}
Class.prototype = Class
class1 = new Class()
class2 = new Class()

// print false 
console.log(class1.test === class2.test)
class1.test['a'] = 2
// print {}
console.log(class2.test)
class2.test['a'] = 2
console.log(global_this)



var global_this = {'test': 2}
Class = function(){
    this.test = {}
    return global_this
}
Class.prototype = Class
class1 = new Class()
class2 = new Class()

// print true 
console.log(class1.test === class2.test)
class1.test['a'] = 2
// print 2
console.log(class2.test)


// prototype chain
function Foo() {
    this.value = 42;
}
Foo.prototype = {
    method: function() {}
};

function Bar() {}

// 设置Bar的prototype属性为Foo的实例对象
Bar.prototype = new Foo();
Bar.prototype.foo = 'Hello World';

// 修正Bar.prototype.constructor为Bar本身
Bar.prototype.constructor = Bar;

var test = new Bar() // 创建Bar的一个新实例


var Cat = {
    createNew: function(){
        // some code here
        return {}
    }
};
cat = Cat.createNew()

afunc = function(){return this;}
b = afunc()
