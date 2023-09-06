//import lib
const express = require('express');
const app = express();
const fs = require('fs');
const PORT = 3000;

//run on localhost:3000/
app.get('/', (req, res) => {
    res.send('/');
});

//run on localhost:3000/data
app.get('/data', (req, res) => {
    //read json file
    fs.readFile('data.json', 'utf8', (err, data) => {
        //catch error
        if (err) {
            res.status(500).send('Error reading file');
            return;
        }
        //set header
        res.setHeader('Content-Type', 'application/json');
        //data content to jsonData (JSON -> Js)
        const jsonData = JSON.parse(data);
        //indent = 4, stringify all data content (Js -> JSON) 
        //jsonData.data would be its data content, jsonData.target would be its target content
        const indentedJson = JSON.stringify(jsonData, null, 4);
        //pass data into api
        res.send(indentedJson);
    });
});
//check running on port
app.listen(PORT, ()=>{
    console.log('running on port 3000')
})
