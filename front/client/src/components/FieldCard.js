import React from 'react';

const FieldCard = ({ field }) => {
    var base = '';
    const handle = (buffer) => {
        var binary = '';
        var bytes = new Uint8Array( buffer );
        var len = bytes.byteLength;
        for (var i = 0; i < len; i++) {
            binary += String.fromCharCode( bytes[ i ] );
        }
        //console.log(window.btoa( binary ));
        base = window.btoa( binary );
        return;
    }
    /*useEffect((field) => {
        console.log(arrayBufferToBase64(field.png));
    }, []);*/

    return (
        <div>
            <button onClick={handle(field.png)}>test</button>
            <li  key={field._id}>
                {field.green} <br/>
                {field.yellow}<br/>
                {field.sizex}<br/>
                {field.sizey}<br/>
                {field.name}<br/>
                <br/>
                <br/>
                <img src={`data:image/jpeg;base64,${field.png}`} alt='fieldata'/>
            </li>
        </div>
    );
};

export default FieldCard;