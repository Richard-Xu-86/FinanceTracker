const renderChat1 = (data1, labels1,type,days) => {
    const ctx1 = document.getElementById('myChart1').getContext('2d');
    const myChart1 = new Chart(ctx1, {
        type: type,
        data: {
            labels: labels1,
            datasets: [{
                label: `Last ${days} expenses`,
                data: data1,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Expenses per category'
            }
        }
    });

};
const renderChat2 = (data2, labels2,type,days) => {
    const ctx2 = document.getElementById('myChart2').getContext('2d');
    const myChart2 = new Chart(ctx2, {
        type: type,
        data: {
            labels: labels2,
            datasets: [{
                label: `Last ${days} income`,
                data: data2,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Income per source'
            }
        }
    });

};

const getChartData=()=>{
    fetch('/lastmonth-data').then(res=>res.json()).then(result=>{
        console.log('result',result)
        const category_data = result.expense_category_amount;
        const [labels1,data1] = [
            Object.keys(category_data),
            Object.values(category_data),
        ];
        const source_data = result.income_source_amount;
        const [labels2,data2] = [
            Object.keys(source_data),
            Object.values(source_data),
        ];
        const type = result.type;
        const days = result.days;
        console.log('type',days)
        renderChat1(data1,labels1,type,days);
        renderChat2(data2,labels2,type,days);
    });
};



document.onload=getChartData();