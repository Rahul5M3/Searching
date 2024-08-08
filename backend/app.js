if(process.env.NODE_ENV!="production"){
    require("dotenv").config();
}
 
const express = require('express');
const cors = require('cors');
const path=require('path');
const ejsMate=require('ejs-mate');
const {spawn}=require('child_process');
const fs = require('fs');

const app=express();
const port = process.env.PORT;

app.use(express.static(path.join(__dirname, '../frontend/public')));
app.set('view engine', 'ejs');
app.engine("ejs",ejsMate);
app.set('views',(path.join(__dirname, '../frontend/views')));

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({extended:true}));

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});

app.get('/',(req,res)=>{
   return res.render('index.ejs');
})

app.post('/searched_query',async (req,res)=>{
    const query=req.body.query;
    if(req.body.query!=""){
        const d= spawn("python",["./models/search.py", query]);
        fs.readFile('.././data/filtered_data_result.json','utf8', async (err, data) => {
        if (err) {
            console.error('Error reading JSON file:', err);
            return res.status(500).send('Error');
        }

        const jsonData = await JSON.parse(data);
        return res.render('result.ejs', { data: jsonData });
        });
    }else {
        fs.readFile('.././data/Data.json','utf8', async (err, data) => {
            if (err) {
                console.error('Error reading JSON file:', err);
                return res.status(500).send('Error');
            }
    
            const jsonData = await JSON.parse(data);
            return res.render('result.ejs', { data: jsonData });
            });
    }
})