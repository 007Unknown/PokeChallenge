function search(name) {
    fetch(`http://localhost:5000/pokemon/?name=${name}`)
        .then(res => {
            if(res.ok) {
                return res.json();
            }
            throw new Error('Not successful')
        })
        .then(data => console.log(data))
        .catch(error => console.error(error))
}

function getValue() {
    return document.getElementById("textBox").value;
}
