const API_URL = "http://127.0.0.1:8000";

console.log("TRACKX USER FRONTEND");
console.log("API:", API_URL);


/* ============================================================
   NAVIGATION
   ============================================================ */

function showSection(sectionId) {

    document.querySelectorAll(".page-section")
        .forEach(section => {
            section.classList.remove("active-section");
        });

    const section = document.getElementById(sectionId);

    if (section) {
        section.classList.add("active-section");
    }

    document.querySelectorAll(".nav-item")
        .forEach(button => {
            button.classList.remove("active");

            const onclick = button.getAttribute("onclick");

            if (onclick &&
                onclick.includes("'" + sectionId + "'")) {
                button.classList.add("active");
            }
        });

    const titles = {
        home: "Welcome to TrackX",
        journey: "Plan Your Journey",
        running: "Trains Running",
        stations: "Metro Stations",
        upcoming: "Upcoming Trains"
    };

    document.getElementById("pageTitle").textContent =
        titles[sectionId] || "TrackX";

    if (sectionId === "running") {
        loadRunningTrains();
    }

    if (sectionId === "stations") {
        loadStations();
    }

    if (sectionId === "upcoming") {
        loadUpcomingTrains();
    }
}


/* ============================================================
   API
   ============================================================ */

async function apiFetch(endpoint, options = {}) {

    const response = await fetch(
        API_URL + endpoint,
        options
    );

    if (!response.ok) {

        let message = `HTTP ${response.status}`;

        try {
            const data = await response.json();

            if (data.detail) {
                message = data.detail;
            }

        } catch (error) {}

        throw new Error(message);
    }

    return await response.json();
}


/* ============================================================
   STATIONS
   ============================================================ */

async function loadStations() {

    const grid =
        document.getElementById("stationGrid");

    try {

        grid.innerHTML =
            `<div class="loading">
                Loading stations...
            </div>`;

        const data =
            await apiFetch("/stations");

        document.getElementById("stationCount")
            .textContent = data.length;

        populateStationDropdowns(data);

        grid.innerHTML = "";

        data.forEach((station, index) => {

            const card =
                document.createElement("div");

            card.className = "station-card";

            card.innerHTML = `
                <div class="station-number">
                    STATION ${String(index + 1).padStart(2, "0")}
                </div>

                <strong>
                    ${escapeHTML(station.station_name)}
                </strong>
            `;

            grid.appendChild(card);
        });

    } catch (error) {

        grid.innerHTML = `
            <div class="empty-state">
                <div>⚠</div>
                <h3>Unable to load stations</h3>
                <p>${escapeHTML(error.message)}</p>
            </div>
        `;

        console.error(error);
    }
}


/* ============================================================
   DROPDOWNS
   ============================================================ */

function populateStationDropdowns(stations) {

    const from =
        document.getElementById("fromStation");

    const to =
        document.getElementById("toStation");

    from.innerHTML =
        `<option value="">Select starting station</option>`;

    to.innerHTML =
        `<option value="">Select destination station</option>`;

    stations.forEach(station => {

        const option1 =
            document.createElement("option");

        option1.value =
            station.station_name;

        option1.textContent =
            station.station_name;

        const option2 =
            document.createElement("option");

        option2.value =
            station.station_name;

        option2.textContent =
            station.station_name;

        from.appendChild(option1);
        to.appendChild(option2);
    });
}


/* ============================================================
   SWAP
   ============================================================ */

function swapStations() {

    const from =
        document.getElementById("fromStation");

    const to =
        document.getElementById("toStation");

    const temp = from.value;

    from.value = to.value;
    to.value = temp;
}


/* ============================================================
   FIND TRAINS
   ============================================================ */

async function findTrains() {

    const from =
        document.getElementById("fromStation").value;

    const to =
        document.getElementById("toStation").value;

    const day =
        document.getElementById("journeyDay").value;

    const time =
        document.getElementById("journeyTime").value;

    const message =
        document.getElementById("journeyMessage");

    const results =
        document.getElementById("trainResults");

    message.className = "message";
    message.textContent = "";

    if (!from || !to) {

        message.textContent =
            "Please select both stations.";

        message.classList.add("error");

        return;
    }

    if (from === to) {

        message.textContent =
            "Starting and destination stations cannot be the same.";

        message.classList.add("error");

        return;
    }

    results.innerHTML =
        `<div class="loading">
            Searching for trains...
        </div>`;

    try {

        const params =
            new URLSearchParams({
                from_station: from,
                to_station: to,
                day: day,
                time: time || "06:00"
            });

        const data =
            await apiFetch(
                `/find-trains?${params.toString()}`
            );

        displayTrainResults(data.results || []);

        if (data.results && data.results.length) {

            message.textContent =
                `${data.results.length} upcoming train(s) found.`;

            message.classList.add("success");

        } else {

            message.textContent =
                "No trains found for the selected time.";

            message.classList.add("error");
        }

    } catch (error) {

        results.innerHTML = `
            <div class="empty-state">
                <div>⚠</div>
                <h3>Could not find trains</h3>
                <p>${escapeHTML(error.message)}</p>
            </div>
        `;

        message.textContent =
            "Unable to connect to TrackX backend.";

        message.classList.add("error");
    }
}


/* ============================================================
   DISPLAY SEARCH RESULTS
   ============================================================ */

function displayTrainResults(trains) {

    const container =
        document.getElementById("trainResults");

    if (!trains.length) {

        container.innerHTML = `
            <div class="empty-state">
                <div>🚆</div>
                <h3>No trains available</h3>
                <p>Try selecting a later time.</p>
            </div>
        `;

        return;
    }

    container.innerHTML = "";

    trains.forEach(train => {

        const card =
            document.createElement("div");

        card.className = "train-result";

        card.innerHTML = `

            <div class="result-time">
                ${escapeHTML(train.departure_time || "--:--")}
            </div>

            <div>
                <div class="train-name">
                    ${escapeHTML(
                        train.train_id || "TRAIN"
                    )}
                </div>

                <div class="route">
                    ${escapeHTML(train.from_station)}
                    →
                    ${escapeHTML(train.to_station)}
                </div>
            </div>

            <div>
                <div class="train-name">
                    ${escapeHTML(
                        train.fleet_type || "RUNNING"
                    )}
                </div>

                <div class="route">
                    Metro service
                </div>
            </div>

            <div>
                <span class="active-badge">
                    ${escapeHTML(
                        train.status || "ACTIVE"
                    )}
                </span>
            </div>
        `;

        container.appendChild(card);
    });
}

/* ============================================================
   LOAD RUNNING TRAINS + LIVE NEXT DEPARTURE
   ============================================================ */

async function loadRunningTrains() {

    const container =
        document.getElementById("runningGrid");

    try {

        container.innerHTML = `
            <div class="loading">
                Loading train schedule...
            </div>
        `;

        /* ----------------------------------------------------
           GET TODAY'S DAY
        ---------------------------------------------------- */

        const day = getCurrentDay();


        /* ----------------------------------------------------
           LOAD TODAY'S SCHEDULE
        ---------------------------------------------------- */

        const data =
            await apiFetch(
                "/train-running?day=" +
                encodeURIComponent(day)
            );


        const trains =
            data.trains || [];


        /* ----------------------------------------------------
           TOTAL SCHEDULED DEPARTURES
        ---------------------------------------------------- */

        const runningCount =
            document.getElementById(
                "runningCount"
            );

        if (runningCount) {

            runningCount.textContent =
                data.total_departures ??
                trains.length;

        }


        container.innerHTML = "";


        /* ----------------------------------------------------
           NO TRAINS
        ---------------------------------------------------- */

        if (!trains.length) {

            container.innerHTML = `

                <div class="empty-state">

                    <div>🚆</div>

                    <h3>
                        No scheduled trains
                    </h3>

                    <p>
                        No train departures are
                        available for ${escapeHTML(day)}.
                    </p>

                </div>

            `;


            updateNextDeparture([]);


            return;

        }


        /* ----------------------------------------------------
           DISPLAY ALL DEPARTURES
        ---------------------------------------------------- */

        trains.forEach(
            (train, index) => {

                const card =
                    document.createElement("div");


                card.className =
                    "train-card";


                const trainId =
                    train.train_id ||
                    train.train ||
                    "TRAIN";


                const departure =
                    train.departure_time ||
                    train.next_departure ||
                    "--:--";


                const from =
                    train.from_station ||
                    "Aluva";


                const to =
                    train.to_station ||
                    "Tripunithura Terminal";


                const fleet =
                    train.fleet_type ||
                    "RUNNING";


                const status =
                    train.status ||
                    "ACTIVE";


                let badgeClass =
                    "train-badge";


                if (
                    status === "UNAVAILABLE"
                ) {

                    badgeClass =
                        "train-badge unavailable";

                }


                card.innerHTML = `

                    <div class="train-card-top">

                        <div>

                            <div class="schedule-number">
                                DEPARTURE #${index + 1}
                            </div>

                            <h3>
                                ${escapeHTML(
                                    trainId
                                )}
                            </h3>

                        </div>


                        <span class="${badgeClass}">
                            ${escapeHTML(
                                status
                            )}
                        </span>

                    </div>


                    <div class="train-route">

                        ${escapeHTML(
                            from
                        )}

                        →

                        ${escapeHTML(
                            to
                        )}

                    </div>


                    <div class="train-departure">

                        <span>
                            DEPARTURE
                        </span>

                        <strong>
                            ${escapeHTML(
                                departure
                            )}
                        </strong>

                    </div>


                    <div class="train-fleet">

                        <span>
                            FLEET
                        </span>

                        <strong>
                            ${escapeHTML(
                                fleet
                            )}
                        </strong>

                    </div>

                `;


                container.appendChild(card);

            }
        );


        /* ----------------------------------------------------
           UPDATE NEXT DEPARTURE
        ---------------------------------------------------- */

        updateNextDeparture(trains);


    } catch (error) {

        console.error(
            "Failed to load running trains:",
            error
        );


        container.innerHTML = `

            <div class="empty-state">

                <div>⚠</div>

                <h3>
                    Train schedule unavailable
                </h3>

                <p>
                    ${escapeHTML(
                        error.message
                    )}
                </p>

            </div>

        `;


        updateNextDeparture([]);

    }

}


/* ============================================================
   FIND NEXT DEPARTURE BASED ON CURRENT TIME
   ============================================================ */

function updateNextDeparture(
    trains
) {

    const nextElement =
        document.getElementById(
            "nextDeparture"
        );


    if (!nextElement) {

        return;

    }


    if (
        !trains ||
        !trains.length
    ) {

        nextElement.textContent =
            "--:--";

        return;

    }


    /* --------------------------------------------------------
       CURRENT TIME
       -------------------------------------------------------- */

    const now =
        new Date();


    const currentMinutes =
        now.getHours() * 60 +
        now.getMinutes() +
        (
            now.getSeconds() / 60
        );


    /* --------------------------------------------------------
       FIND FIRST DEPARTURE AFTER CURRENT TIME
       -------------------------------------------------------- */

    let nextTrain = null;


    for (
        const train of trains
    ) {

        const departure =
            train.departure_time ||
            train.next_departure;


        if (!departure) {

            continue;

        }


        const departureMinutes =
            timeToMinutesFrontend(
                departure
            );


        if (
            departureMinutes >
            currentMinutes
        ) {

            nextTrain = train;

            break;

        }

    }


    /* --------------------------------------------------------
       NO MORE TRAINS TODAY
       -------------------------------------------------------- */

    if (!nextTrain) {

        nextElement.textContent =
            "No more trains";

        return;

    }


    /* --------------------------------------------------------
       SHOW NEXT DEPARTURE
       -------------------------------------------------------- */

    nextElement.textContent =
        nextTrain.departure_time ||
        nextTrain.next_departure ||
        "--:--";

}


/* ============================================================
   CONVERT HH:MM / HH:MM:SS TO MINUTES
   ============================================================ */

function timeToMinutesFrontend(
    value
) {

    if (!value) {

        return 0;

    }


    const parts =
        String(value)
            .split(":");


    const hour =
        parseInt(
            parts[0],
            10
        ) || 0;


    const minute =
        parseInt(
            parts[1],
            10
        ) || 0;


    const second =
        parseInt(
            parts[2],
            10
        ) || 0;


    return (
        hour * 60 +
        minute +
        second / 60
    );

}


/* ============================================================
   LIVE NEXT-DEPARTURE REFRESH
   ============================================================ */

function startNextDepartureTimer() {

    /* --------------------------------------------------------
       Update every 30 seconds
       -------------------------------------------------------- */

    setInterval(
        async function () {

            try {

                const day =
                    getCurrentDay();


                const data =
                    await apiFetch(
                        "/train-running?day=" +
                        encodeURIComponent(day)
                    );


                updateNextDeparture(
                    data.trains || []
                );


            } catch (error) {

                console.error(
                    "Next departure update failed:",
                    error
                );

            }

        },
        30000
    );

}

/* ============================================================
   UPCOMING SCHEDULE
   ============================================================ */

async function loadUpcomingTrains() {

    const container =
        document.getElementById("upcomingList");

    const day =
        document.getElementById("scheduleDay").value;

    try {

        container.innerHTML =
            `<div class="loading">
                Loading AI schedule...
            </div>`;

        const data =
            await apiFetch(
                `/schedule?day=${encodeURIComponent(day)}`
            );

        const schedule =
            data.schedule || [];

        container.innerHTML = "";

        if (!schedule.length) {

            container.innerHTML = `
                <div class="empty-state">
                    <div>◷</div>
                    <h3>No schedule available</h3>
                    <p>No schedule found for ${escapeHTML(day)}.</p>
                </div>
            `;

            return;
        }

        /*
         * IMPORTANT:
         * Do NOT use slice(0, 50).
         * The complete schedule is displayed.
         */

        schedule.forEach(train => {

            const row =
                document.createElement("div");

            row.className = "schedule-row";

            row.innerHTML = `

                <div class="schedule-time">
                    ${escapeHTML(
                        train.departure_time || "--:--"
                    )}
                </div>

                <div class="schedule-train">
                    ${escapeHTML(
                        train.train_id || "TRAIN"
                    )}
                </div>

                <div class="schedule-route">
                    ${escapeHTML(
                        train.from_station || "Aluva"
                    )}
                </div>

                <div class="schedule-route">
                    →
                    ${escapeHTML(
                        train.to_station ||
                        "Tripunithura Terminal"
                    )}
                </div>

                <div class="schedule-status">
                    ${escapeHTML(
                        train.status || "ACTIVE"
                    )}
                </div>
            `;

            container.appendChild(row);
        });

    } catch (error) {

        container.innerHTML = `
            <div class="empty-state">
                <div>⚠</div>
                <h3>Schedule unavailable</h3>
                <p>${escapeHTML(error.message)}</p>
            </div>
        `;

        console.error(error);
    }
}


/* ============================================================
   CURRENT DAY
   ============================================================ */

function getCurrentDay() {

    const days = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ];

    return days[new Date().getDay()];
}


function setupCurrentDay() {

    const day = getCurrentDay();

    document.getElementById("currentDay")
        .textContent = day;

    document.getElementById("journeyDay")
        .value = day;

    document.getElementById("scheduleDay")
        .value = day;
}


/* ============================================================
   BACKEND
   ============================================================ */

async function checkBackend() {

    const status =
        document.getElementById("backendStatus");

    try {

        const data =
            await apiFetch("/");

        console.log(
            "TrackX backend connected:",
            data
        );

        status.className =
            "backend-status online";

        status.innerHTML = `
            <span class="status-dot"></span>
            TRACKX SYSTEM ONLINE
        `;

        return true;

    } catch (error) {

        status.className =
            "backend-status offline";

        status.innerHTML = `
            <span class="status-dot"></span>
            BACKEND OFFLINE
        `;

        return false;
    }
}


/* ============================================================
   ESCAPE HTML
   ============================================================ */

function escapeHTML(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/* ============================================================
   INITIALIZE
   ============================================================ */

async function initializeTrackX() {

    setupCurrentDay();

    await checkBackend();

    await loadStations();

    await loadRunningTrains();
}


document.addEventListener(
    "DOMContentLoaded",
    initializeTrackX
);