var obj = {}, initValue = true;
Object.defineProperty(obj, 'newKey', {
    get: function () {
        return initValue;
    },
    set: function (value) {
        initValue = value;
    }
});
// 点击改变布尔值为false
document.getElementById('btncc').onclick = function () {
    initValue = false;
    console.log(123);
}

// 通过延时器我已经知道，已被改变
setTimeout(() => {
    console.log(obj.newKey)
}, 3000)
// 抛出我所需要的函数和对象，然后将obj.newKey赋予msg，然后通过watch监听，看是否有变化，但是这里的监听好像没起作用
export default {
    con, obj
}