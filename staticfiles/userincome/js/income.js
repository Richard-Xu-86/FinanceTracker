const searchField = document.querySelector('#searchfield');
const tableOutput = document.querySelector('.table-search');
const tableStart = document.querySelector('.table-start');
const pagenation = document.querySelector('.pagenation-container');
const noResults = document.querySelector(".no-results");
const tBody = document.querySelector('.t-body');

tableOutput.style.display = "none";

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;

    if(searchValue.length > 0){
        tBody.innerHTML="";
        pagenation.style.display = "none";
        fetch("/income/search-income",{
            body:JSON.stringify({ searchText : searchValue}),method:"POST",
        }).then(res=>res.json()).then(data=>{
            console.log('data',data);
            tableStart.style.display = "none";
            tableOutput.style.display = "block";
            if(data.length ===0){
                noResults.style.display = "block";
                tableOutput.style.display = "none";
            }else{
                tBody.innerHTML="";
                noResults.style.display = "none";
                data.forEach((item) => {
                    tBody.innerHTML +=`
                    <tr>
                    <td>${item.amount}</td>
                    <td>${item.source}</td>
                    <td>${item.decription}</td>
                    <td>${item.date}</td>
                    <td><a class="btn btn-secondary btn-sm" href="income/income-edit/${item.id}">Edit</a></td>
                    </tr>`;
                });
            }
        });
    }else{
        tableOutput.style.display = "none";
        tableStart.style.display = "block";
        pagenation.style.display = "flex"; 
    }
});