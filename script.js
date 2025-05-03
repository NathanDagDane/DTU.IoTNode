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
    const response = await fetch('/set/' + state);
}

async function liveFetch() {
    if (!live) return;
    await fetchData('/data');
}

var liveTimer = setInterval(liveFetch, 400); // Update every 200ms
window.onload = fetchData;

function toggleLive() {
    live = !live;
    if (live) {
        var liveTimer = setInterval(liveFetch, 400);
    }
    else{
        clearInterval(liveTimer);
    }
}

function updateColor() {
    const hue = parseInt(hueSlider.value, 10);
    const saturation = parseInt(saturationSlider.value, 10);
    const brightness = 50

    const [r, g, b] = hsvToRgb(hue, saturation, brightness);
    console.log(r, g, b);
    setState('RGB-Red/'   + r/128);
    setState('RGB-Green/' + g/128);
    setState('RGB-Blue/'  + b/128);

    document.body.style.setProperty('--colour-acc', 'hsl(' + hue + ', ' + saturation + '%, 50%)');
}

function hsvToRgb(h, s, v) {
    s /= 100; v /= 100;
    let c = v * s; let x = c * (1 - Math.abs((h / 60) % 2 - 1)); let m = v - c;
    let r = 0, g = 0, b = 0;

    if (h < 60) [r, g, b] = [c, x, 0];
    else if (h < 120) [r, g, b] = [x, c, 0];
    else if (h < 180) [r, g, b] = [0, c, x];
    else if (h < 240) [r, g, b] = [0, x, c];
    else if (h < 300) [r, g, b] = [x, 0, c];
    else [r, g, b] = [c, 0, x];

    return [Math.round((r + m) * 255), Math.round((g + m) * 255), Math.round((b + m) * 255)];
}

// Only update on slider release (mouse up or touch end)
hueSlider.addEventListener("change", updateColor); saturationSlider.addEventListener("change", updateColor);

updateColor(); // initial