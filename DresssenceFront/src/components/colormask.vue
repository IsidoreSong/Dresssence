<template>
    <div id='mask'
    :style="{left:position['left']+'px',top:position['top']+'px',width:position['width']+'px',height:position['height']+'px'}">
    </div>
</template>

<script>
export default {
    name: "colorMask",
    props:['position'],
}
</script>

<style scope>
#mask {
    position:absolute;
    border:2px solid skyblue;
    background-color: rgba(96,166,221,0.3);
}
</style>


