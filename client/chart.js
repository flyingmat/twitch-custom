var data = {
    labels: [],
    datasets: [{
        label: 'All messages',
        data: [],
        borderColor: 'rgb(75, 192, 192)',
    }],
};

var config = {
    type: 'line',
    data: data,
    options: {
        normalized: true,
        animation: false,
        spanGaps: true,
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                min: 0,
            }
        },
        elements: {
            line: {
                tension: .6,
            },
            point: {
                radius: 0,
            }
        },
        plugins: {
            zoom: {
                zoom: {
                    wheel: {
                        enabled: true,
                    },
                    pinch: {
                        enabled: true
                    },
                    mode: 'x',
                },
                pan: {
                    enabled: true,
                    mode: 'x',
                }
            },
            decimation: {
                enabled: true,
                algorithm: 'min-max',
            },
            legend: {
                display: false
            },
            tooltips: {
                enabled: false
            },
        }
    }
};
