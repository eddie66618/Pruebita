<template>
        <div class="main">
            <div class="imgLogo">
                <img src="../../assets/logo_cnsr.png" alt="" width="260" height="80">
            </div>
            <div class="container">
                <div class="form">
                    <div class="title"> 
                        <h3>Conteste las preguntas</h3>
                    </div>
                    <p v-if="errors.length" style="color: red;">
                        <b>Corrija los siguientes errores</b>
                        <ul>
                        <li v-for="error in errors">{{ error }}</li>
                        </ul>
                    </p>
                    <form @submit="checkForm">
                    <div class="inputDiv">
                        <label><svg xmlns="http://www.w3.org/2000/svg" height="0.7em" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM169.8 165.3c7.9-22.3 29.1-37.3 52.8-37.3h58.3c34.9 0 63.1 28.3 63.1 63.1c0 22.6-12.1 43.5-31.7 54.8L280 264.4c-.2 13-10.9 23.6-24 23.6c-13.3 0-24-10.7-24-24V250.5c0-8.6 4.6-16.5 12.1-20.8l44.3-25.4c4.7-2.7 7.6-7.7 7.6-13.1c0-8.4-6.8-15.1-15.1-15.1H222.6c-3.4 0-6.4 2.1-7.5 5.3l-.4 1.2c-4.4 12.5-18.2 19-30.6 14.6s-19-18.2-14.6-30.6l.4-1.2zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/></svg>  Pregunta 1</label>
                        <input class="inputForm" type="text" v-model="p1">
                    </div>
                    <div class="inputDiv" >
                        <label><svg xmlns="http://www.w3.org/2000/svg" height="0.7em" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM169.8 165.3c7.9-22.3 29.1-37.3 52.8-37.3h58.3c34.9 0 63.1 28.3 63.1 63.1c0 22.6-12.1 43.5-31.7 54.8L280 264.4c-.2 13-10.9 23.6-24 23.6c-13.3 0-24-10.7-24-24V250.5c0-8.6 4.6-16.5 12.1-20.8l44.3-25.4c4.7-2.7 7.6-7.7 7.6-13.1c0-8.4-6.8-15.1-15.1-15.1H222.6c-3.4 0-6.4 2.1-7.5 5.3l-.4 1.2c-4.4 12.5-18.2 19-30.6 14.6s-19-18.2-14.6-30.6l.4-1.2zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/></svg>  Pregunta 1</label>
                        <input type="text" class="inputForm" v-model="p2">
                    </div>
                    <div class="inputDiv" >
                        <label><svg xmlns="http://www.w3.org/2000/svg" height="0.7em" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM169.8 165.3c7.9-22.3 29.1-37.3 52.8-37.3h58.3c34.9 0 63.1 28.3 63.1 63.1c0 22.6-12.1 43.5-31.7 54.8L280 264.4c-.2 13-10.9 23.6-24 23.6c-13.3 0-24-10.7-24-24V250.5c0-8.6 4.6-16.5 12.1-20.8l44.3-25.4c4.7-2.7 7.6-7.7 7.6-13.1c0-8.4-6.8-15.1-15.1-15.1H222.6c-3.4 0-6.4 2.1-7.5 5.3l-.4 1.2c-4.4 12.5-18.2 19-30.6 14.6s-19-18.2-14.6-30.6l.4-1.2zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/></svg>  Pregunta 1</label>
                        <input type="text" class="inputForm" v-model="p3">
                    </div>
                    <div class="inputDiv" >
                        <label><svg xmlns="http://www.w3.org/2000/svg" height="0.7em" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM169.8 165.3c7.9-22.3 29.1-37.3 52.8-37.3h58.3c34.9 0 63.1 28.3 63.1 63.1c0 22.6-12.1 43.5-31.7 54.8L280 264.4c-.2 13-10.9 23.6-24 23.6c-13.3 0-24-10.7-24-24V250.5c0-8.6 4.6-16.5 12.1-20.8l44.3-25.4c4.7-2.7 7.6-7.7 7.6-13.1c0-8.4-6.8-15.1-15.1-15.1H222.6c-3.4 0-6.4 2.1-7.5 5.3l-.4 1.2c-4.4 12.5-18.2 19-30.6 14.6s-19-18.2-14.6-30.6l.4-1.2zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/></svg>  Pregunta 1</label>
                        <input type="text" class="inputForm" v-model="p4">
                    </div>
                    <div class="inputDiv" > 
                        <input class="inputSubmit" type="submit" >
                    </div>
                </form>
                </div>
                <div class="bg" >
                    <img class="imgto" src="../../assets/typing2.png"  alt="">
                </div>
            </div>
        </div>
</template>

<style scoped>
.main{
    width: 100vw;
    height: 100vh;
    background-color: white;
}
.title {
    text-align: center;
    color: #0077c8;
    font-weight: bold;
    font-size: 20px;
    padding-bottom: 10px;
}
.imgLogo {
    margin-top: 20px;
    margin-left: 20px;
    position: absolute;
    top: 0;
    left: 0
}
.inputDiv{
    padding: 2%;
}
.container{
    display: flex;
    justify-content: center;
    align-items: center;
}
.form{
    width: 100vw;
    height: 100vh;
    max-width: 100vw;
    background-color:#fff;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.inputForm{
    border-radius: 0;
    display: block;
    border: none;
    border-bottom: 2px solid #0077c8;
    outline: none;   
    width: 35vw;
    padding: 1.4%;
}
.inputSubmit{
    background-color: #A1CE57;
    color:white;
    width: 35vw;
    padding: 2%;
    border-radius: 10px;
}
.imgto{
    width: 45vw;
}
.inputForm:focus {
    border-bottom: 2.5px solid #0077c8;
}
.inputSubmit:hover{
    opacity: 0.9;
}
.bg
{
    width: 100vw;
    height: 100vh;
    background-color: #4c9fd8;
    border-top-left-radius: 900px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
}
@media screen and ( max-width:830px){
    .bg{
        display: none;
    }
    .form{
        border: 1px solid #ccc;
        width: fit-content;
        height: fit-content;
        padding: 5%;
        margin-top: 14vh;
        border-radius: 20px;
        box-shadow: 1px 1px 1px 1px #ccc;
    }
    .inputDiv{
        padding:  2% 0;
    }
}

</style>
<script>
export default {
    data(){
        return{
            p1:'',
            p2:'',
            p3:'',
            p4:'',
            errors: [],

        }
    },
    methods:{
        checkForm(){
            this.errors = [];
            if (!this.p1) {
                this.errors.push('Complete la pregunta 1');
            }
            if(!this.p2){
                this.errors.push("Complete la pregunta 2");
            }
            if(!this.p3){
                this.errors.push("Complete la pregunta 3");
            }
            if(!this.p4){
                this.errors.push("Complete la pregunta 4");
            }
               
               
        },
    }

}
</script>
