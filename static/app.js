document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const originSelect = document.getElementById('originSelect');
    const destSelect = document.getElementById('destSelect');
    const swapBtn = document.getElementById('swapBtn');
    const departureDate = document.getElementById('departureDate');
    const minBufferRange = document.getElementById('minBufferRange');
    const maxBufferRange = document.getElementById('maxBufferRange');
    const minBufferVal = document.getElementById('minBufferVal');
    const maxBufferVal = document.getElementById('maxBufferVal');
    const sortBySelect = document.getElementById('sortBySelect');
    const searchForm = document.getElementById('searchForm');

    // UI State Elements
    const routeCountBadge = document.getElementById('routeCountBadge');
    const summaryStats = document.getElementById('summaryStats');
    const statTotal = document.getElementById('statTotal');
    const statDirect = document.getElementById('statDirect');
    const statConnecting = document.getElementById('statConnecting');
    const statJunctions = document.getElementById('statJunctions');

    const loadingState = document.getElementById('loadingState');
    const emptyState = document.getElementById('emptyState');
    const routesList = document.getElementById('routesList');
    const networkCanvas = document.getElementById('networkCanvas');

    // Global variables
    let stationData = [];
    let networkGraphData = null;

    // Initialize Default Date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    departureDate.value = tomorrow.toISOString().split('T')[0];

    // Range Slider Live Listeners
    minBufferRange.addEventListener('input', (e) => {
        minBufferVal.textContent = `${e.target.value} Mins`;
    });

    maxBufferRange.addEventListener('input', (e) => {
        const mins = parseInt(e.target.value);
        const hours = (mins / 60).toFixed(1);
        maxBufferVal.textContent = `${hours} Hours`;
    });

    // Swap Origin & Destination
    swapBtn.addEventListener('click', () => {
        const temp = originSelect.value;
        originSelect.value = destSelect.value;
        destSelect.value = temp;
    });

    // Tab Navigation
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const targetTab = btn.getAttribute('data-tab');
            document.getElementById(targetTab).classList.add('active');

            if (targetTab === 'networkTab') {
                renderNetworkCanvas();
            }
        });
    });

    // Fetch Stations List
    async function loadStations() {
        try {
            const res = await fetch('/api/stations');
            stationData = await res.json();

            originSelect.innerHTML = '<option value="" disabled>Select origin station...</option>';
            destSelect.innerHTML = '<option value="" disabled>Select destination station...</option>';

            stationData.forEach(st => {
                const juncPill = st.is_junction ? ' (Junction)' : '';
                const opt1 = new Option(`${st.city} - ${st.name} [${st.code}]${juncPill}`, st.code);
                const opt2 = new Option(`${st.city} - ${st.name} [${st.code}]${juncPill}`, st.code);
                originSelect.add(opt1);
                destSelect.add(opt2);
            });

            // Set default search (New Delhi -> KSR Bengaluru)
            originSelect.value = 'NDLS';
            destSelect.value = 'SBC';

            // Trigger initial search
            fetchRoutes();
        } catch (err) {
            console.error('Failed to load stations:', err);
        }
    }

    // Fetch Network Graph for Canvas
    async function loadNetworkGraph() {
        try {
            const res = await fetch('/api/network');
            networkGraphData = await res.json();
        } catch (err) {
            console.error('Failed to load network graph:', err);
        }
    }

    // Handle Form Submit
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        fetchRoutes();
    });

    // Fetch Routes API Call
    async function fetchRoutes() {
        const origin = originSelect.value;
        const destination = destSelect.value;

        if (!origin || !destination) {
            alert('Please select both Origin and Destination stations.');
            return;
        }

        if (origin === destination) {
            alert('Origin and Destination cannot be the same station.');
            return;
        }

        // Show Loading State
        emptyState.classList.add('hidden');
        routesList.innerHTML = '';
        loadingState.classList.remove('hidden');
        summaryStats.classList.add('hidden');

        const payload = {
            origin: origin,
            destination: destination,
            departure_date: departureDate.value,
            min_buffer_mins: parseInt(minBufferRange.value),
            max_buffer_mins: parseInt(maxBufferRange.value),
            sort_by: sortBySelect.value
        };

        try {
            const res = await fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || 'Search request failed.');
            }

            const data = await res.json();
            renderRouteResults(data);
        } catch (err) {
            alert(`Error: ${err.message}`);
        } finally {
            loadingState.classList.add('hidden');
        }
    }

    // Render Route Cards Logic
    function renderRouteResults(data) {
        const routes = data.routes || [];
        routeCountBadge.textContent = routes.length;

        // Update Summary Stats
        statTotal.textContent = data.total_routes_found;
        statDirect.textContent = data.direct_routes_count;
        statConnecting.textContent = data.connecting_routes_count;

        // Extract unique candidate junctions
        const junctionsSet = new Set(
            routes
                .filter(r => r.type === '1-STOP CONNECTING')
                .map(r => r.junction.name)
        );
        statJunctions.textContent = junctionsSet.size;

        summaryStats.classList.remove('hidden');

        if (routes.length === 0) {
            emptyState.innerHTML = `
                <div class="state-icon">❌</div>
                <h3>No Matching Routes Found</h3>
                <p>Try adjusting your transfer layover buffer slider (${minBufferRange.value}m – ${maxBufferVal.textContent}) or selecting a different departure date.</p>
            `;
            emptyState.classList.remove('hidden');
            return;
        }

        routesList.innerHTML = '';

        routes.forEach(route => {
            const card = document.createElement('div');
            card.className = 'route-card';

            const isDirect = route.type === 'DIRECT';
            const durationFormatted = formatDuration(route.total_duration_mins);

            let html = `
                <div class="route-header">
                    <div class="route-badges">
                        <span class="type-pill ${isDirect ? 'type-direct' : 'type-connecting'}">
                            ${isDirect ? '⚡ DIRECT TRAIN' : '🔀 1-STOP CONNECTING'}
                        </span>
                    </div>
                    <div class="route-metrics">
                        <div class="metric-item">
                            <span>Total Duration:</span>
                            <span class="metric-val">${durationFormatted}</span>
                        </div>
                        <div class="metric-item">
                            <span>Est. Fare:</span>
                            <span class="metric-val">₹ ${route.total_fare}</span>
                        </div>
                    </div>
                </div>

                <div class="timeline-container">
            `;

            // Render Legs
            route.legs.forEach((leg, idx) => {
                html += `
                    <div class="timeline-leg">
                        <div class="station-node">
                            <span class="station-code">${leg.from_station}</span>
                            <span class="station-name">${leg.from_station_name}</span>
                            <span class="station-time">${formatTime(leg.departure)}</span>
                            <span class="platform-badge">Platform ${leg.departure_platform}</span>
                        </div>

                        <div class="train-info">
                            <span class="train-no">Train #${leg.train_no}</span>
                            <span class="train-name">${leg.train_name}</span>
                            <span class="train-type">${leg.train_type} • ${leg.distance_km} km</span>
                        </div>

                        <div class="station-node" style="text-align: right;">
                            <span class="station-code">${leg.to_station}</span>
                            <span class="station-name">${leg.to_station_name}</span>
                            <span class="station-time">${formatTime(leg.arrival)}</span>
                            <span class="platform-badge">Platform ${leg.arrival_platform}</span>
                        </div>
                    </div>
                `;

                // If connecting route and leg 1, insert Layover Node
                if (!isDirect && idx === 0) {
                    const layoverMins = route.layover_mins;
                    const layoverFormatted = formatDuration(layoverMins);
                    html += `
                        <div class="layover-divider">
                            <div class="layover-pill">
                                <span>⏳ ${layoverFormatted} Layover at ${route.junction.name} [${route.junction.code}]</span>
                            </div>
                        </div>
                    `;
                }
            });

            html += `</div>`;
            card.innerHTML = html;
            routesList.appendChild(card);
        });
    }

    // Helper Functions for Time Formatting
    function formatDuration(totalMins) {
        const hours = Math.floor(totalMins / 60);
        const mins = totalMins % 60;
        return `${hours}h ${mins}m`;
    }

    function formatTime(dtStr) {
        if (!dtStr) return '';
        const parts = dtStr.split(' ');
        if (parts.length < 2) return dtStr;
        return `${parts[1]} (${parts[0].slice(5)})`;
    }

    // Render Canvas Railway Network Graph
    function renderNetworkCanvas() {
        if (!networkCanvas || !networkGraphData) return;

        const ctx = networkCanvas.getContext('2d');
        const rect = networkCanvas.parentElement.getBoundingClientRect();
        networkCanvas.width = rect.width;
        networkCanvas.height = rect.height;

        const width = networkCanvas.width;
        const height = networkCanvas.height;

        ctx.clearRect(0, 0, width, height);

        const nodes = networkGraphData.nodes || [];
        const edges = networkGraphData.edges || [];

        if (nodes.length === 0) return;

        // Map station coordinates to canvas dimensions
        let minLat = 90, maxLat = -90, minLng = 180, maxLng = -180;
        nodes.forEach(n => {
            if (n.lat < minLat) minLat = n.lat;
            if (n.lat > maxLat) maxLat = n.lat;
            if (n.lng < minLng) minLng = n.lng;
            if (n.lng > maxLng) maxLng = n.lng;
        });

        const padding = 60;
        const coordsMap = {};

        nodes.forEach(n => {
            const x = padding + ((n.lng - minLng) / (maxLng - minLng || 1)) * (width - 2 * padding);
            // Flip latitude so north is up
            const y = height - (padding + ((n.lat - minLat) / (maxLat - minLat || 1)) * (height - 2 * padding));
            coordsMap[n.code] = { x, y, name: n.name, isJunction: n.is_junction };
        });

        // Draw Edges
        ctx.lineWidth = 2;
        ctx.strokeStyle = 'rgba(79, 172, 254, 0.25)';
        edges.forEach(e => {
            const p1 = coordsMap[e.source];
            const p2 = coordsMap[e.target];
            if (p1 && p2) {
                ctx.beginPath();
                ctx.moveTo(p1.x, p1.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.stroke();
            }
        });

        // Draw Nodes
        nodes.forEach(n => {
            const p = coordsMap[n.code];
            if (!p) return;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.isJunction ? 8 : 5, 0, 2 * Math.PI);
            
            if (p.isJunction) {
                ctx.fillStyle = '#00f2fe';
                ctx.shadowColor = '#00f2fe';
                ctx.shadowBlur = 10;
            } else {
                ctx.fillStyle = '#4facfe';
                ctx.shadowBlur = 0;
            }
            ctx.fill();

            // Station Code & Name Label
            ctx.shadowBlur = 0;
            ctx.font = p.isJunction ? 'bold 11px Outfit, sans-serif' : '10px Inter, sans-serif';
            ctx.fillStyle = '#f1f5f9';
            ctx.fillText(n.code, p.x + 10, p.y + 4);
        });
    }

    // Initial Loads
    loadStations();
    loadNetworkGraph();

    window.addEventListener('resize', renderNetworkCanvas);
});
