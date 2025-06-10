let myChart = null;  // Global so we can destroy and re-create it

const renderChart = (data, labels, type) => {
    const ctx = document.getElementById('myChart').getContext('2d');

    // Destroy previous chart if it exists
    if (myChart !== null) {
        myChart.destroy();
    }
    myChart = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: 'Last 6 months expenses',
                data: data,
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
            plugins: {
                title: {
                    display: true,
                    text: 'Expense per category'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

};

const getChartData=()=>{
    fetch("/expenses/expenses_summary").then(res=>res.json()).then(result=>{
        console.log('result',result)
        const expense_data = result.expense_category_amount;
        const [labels,data] = [
            Object.keys(expense_data),
            Object.values(expense_data),
        ];
        const selectedType = document.getElementById('graph').value;
        renderChart(data, labels, selectedType);
    });
};



window.addEventListener('DOMContentLoaded', () => {
    getChartData();

    // Re-render chart when dropdown value changes
    const graphSelect = document.getElementById('graph');
    if (graphSelect) {
        graphSelect.addEventListener('change', () => {
            getChartData();
        });
    }
});