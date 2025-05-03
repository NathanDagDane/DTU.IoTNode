const hueSlider = document.getElementById("hue");
const saturationSlider = document.getElementById("saturation");
let live = true;

async function fetchData(endpoint) {
    try {
        const response = await fetch(endpoint);
        const data = await response.json();
        const tbody = document.getElementById('pinTableBody');
        tbody.innerHTML = '';

        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${row.name}</td><td>${row.pin}</td><td>${row.value.toFixed(2)}</td>`;
            tbody.appendChild(tr);

            // Set CSS variable for each pin name
            const variableName = `--${row.name}-val`;
            document.documentElement.style.setProperty(variableName, row.value);
        });
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

async function setState(state) {
    const response = await fetch(state);
}

async function liveFetch() {
    if (!live) return;
    await fetchData('/data');
}

var liveTimer = setInterval(liveFetch, 300); // Update every 200ms
window.onload = fetchData;

function toggleLive() {
    live = !live;
    if (live) {
        var liveTimer = setInterval(liveFetch, 300);
    }
    else{
        clearInterval(liveTimer);
    }
}

function updateColor() {
    const hue = parseInt(hueSlider.value, 10);
    const saturation = parseInt(saturationSlider.value, 10);
    const brightness = 50

    //const [r, g, b] = hsvToRgb(hue, saturation, brightness);
    //const rgb = `rgb(${r}, ${g}, ${b})`;

    document.body.style.setProperty('--colour-acc', 'hsl(' + hue + ', ' + saturation + '%, 50%)');
}

// Only update on slider release (mouse up or touch end)
hueSlider.addEventListener("change", updateColor); saturationSlider.addEventListener("change", updateColor);

updateColor(); // initial