function getNews(){
    let query = document.getElementById("query-input").value
    query = query.split(' ').join('+')
    
    if(query.length==0){
        document.getElementById("query-output").textContent = "Please enter a query"
        document.getElementById("query-output").rows = 2
        document.getElementById("query-output").cols = "Please enter a query".length

        return false
    }

    fetch(`/news/${query}`).then(res => {
        return res.json()
    })
    .then(res => {
        res = res[0]
        const textedJSON = JSON.stringify(res, undefined, 4)
        let maxLength = 0
        Object.keys(res).map(key => {
            if(key.length + res[key].length > maxLength){
                maxLength = key.length + res[key].length
            }
        })
        maxLength = maxLength + 10   
        document.getElementById("query-output").textContent = textedJSON
        document.getElementById("query-output").rows = 5
        document.getElementById("query-output").cols = maxLength
    })
    .catch(err => {
        console.log(err)
        document.getElementById("query-output").textContent = "There was a server error"
        document.getElementById("query-output").rows = 2
        document.getElementById("query-output").cols = "There was a server error".length
    })

    return false
}