const API_URL =
    "https://trackx-backend-nf6f.onrender.com";

console.log("TRACKX USER FRONTEND");
console.log("API:", API_URL);


/* ============================================================
   GLOBAL RUNNING DIRECTION
   ============================================================ */

let runningDirection =
    "ALUVA_TO_TRIPUNITHURA";


/* ============================================================
   NAVIGATION
   ============================================================ */

function showSection(sectionId) {

    document.querySelectorAll(".page-section")
        .forEach(section => {

            section.classList.remove(
                "active-section"
            );

        });


    const section =
        document.getElementById(sectionId);


    if (section) {

        section.classList.add(
            "active-section"
        );

    }


    document.querySelectorAll(".nav-item")
        .forEach(button => {

            button.classList.remove("active");


            const onclick =
                button.getAttribute("onclick");


            if (
                onclick &&
                onclick.includes(
                    "'" + sectionId + "'"
                )
            ) {

                button.classList.add("active");

            }

        });


    const titles = {

        home:
            "Welcome to TrackX",

        journey:
            "Plan Your Journey",

        running:
            "Trains Running",

        stations:
            "Metro Stations",

        upcoming:
            "Upcoming Trains"

    };


    const pageTitle =
        document.getElementById(
            "pageTitle"
        );


    if (pageTitle) {

        pageTitle.textContent =
            titles[sectionId] ||
            "TrackX";

    }


    /* --------------------------------------------------------
       LOAD SECTION DATA
       -------------------------------------------------------- */

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
   API FETCH
   ============================================================ */

async function apiFetch(
    endpoint,
    options = {}
) {

    const response =
        await fetch(
            API_URL + endpoint,
            options
        );


    if (!response.ok) {

        let message =
            `HTTP ${response.status}`;


        try {

            const data =
                await response.json();


            if (data.detail) {

                message =
                    data.detail;

            }

        } catch (error) {

            // Ignore JSON parsing error

        }


        throw new Error(message);

    }


    return await response.json();

}


/* ============================================================
   RUNNING DIRECTION
   ============================================================ */

function setRunningDirection(
    direction
) {

    const validDirections = [

        "ALUVA_TO_TRIPUNITHURA",

        "TRIPUNITHURA_TO_ALUVA"

    ];


    if (
        !validDirections.includes(
            direction
        )
    ) {

        direction =
            "ALUVA_TO_TRIPUNITHURA";

    }


    runningDirection =
        direction;


    const outboundBtn =
        document.getElementById(
            "outboundRunningBtn"
        );


    const returnBtn =
        document.getElementById(
            "returnRunningBtn"
        );


    if (outboundBtn) {

        outboundBtn.classList.toggle(

            "active",

            direction ===
            "ALUVA_TO_TRIPUNITHURA"

        );

    }


    if (returnBtn) {

        returnBtn.classList.toggle(

            "active",

            direction ===
            "TRIPUNITHURA_TO_ALUVA"

        );

    }


    /*
     * Only load when the page is actually available.
     */

    if (
        document.getElementById(
            "runningGrid"
        )
    ) {

        loadRunningTrains();

    }

}


/* ============================================================
   STATIONS
   ============================================================ */

async function loadStations() {

    /*
     * IMPORTANT:
     *
     * Your current index.html does NOT contain
     * stationGrid.
     *
     * Therefore we must NOT use:
     *
     * grid.innerHTML
     *
     * unless the element actually exists.
     */

    const grid =
        document.getElementById(
            "stationGrid"
        );


    try {

        const data =
            await apiFetch(
                "/stations"
            );


        /*
         * Backend may return:
         *
         * [
         *   {id: 1, station_name: "Aluva"},
         *   ...
         * ]
         *
         * or:
         *
         * {stations: [...]}
         */

        const stations =
            Array.isArray(data)

                ? data

                : (
                    data.stations ||
                    []
                );


        /*
         * Update station count.
         */

        document
            .querySelectorAll(
                "#stationCount"
            )
            .forEach(element => {

                element.textContent =
                    stations.length;

            });


        /*
         * Populate journey dropdowns.
         */

        populateStationDropdowns(
            stations
        );


        /*
         * Only render station cards if
         * stationGrid actually exists.
         */

        if (!grid) {

            console.log(
                "stationGrid not found. " +
                "Skipping station cards."
            );

            return;

        }


        grid.innerHTML = "";


        stations.forEach(
            (station, index) => {

                const card =
                    document.createElement(
                        "div"
                    );


                card.className =
                    "station-card";


                card.innerHTML = `

                    <div class="station-number">
                        STATION ${String(
                            index + 1
                        ).padStart(2, "0")}
                    </div>

                    <strong>
                        ${escapeHTML(
                            station.station_name
                        )}
                    </strong>

                `;


                grid.appendChild(
                    card
                );

            }
        );


    } catch (error) {

        console.error(
            "Failed to load stations:",
            error
        );


        /*
         * Do NOT crash the whole application
         * if the station card container is absent.
         */

        if (grid) {

            grid.innerHTML = `

                <div class="empty-state">

                    <div>⚠</div>

                    <h3>
                        Unable to load stations
                    </h3>

                    <p>
                        ${escapeHTML(
                            error.message
                        )}
                    </p>

                </div>

            `;

        }

    }

}


/* ============================================================
   STATION DROPDOWNS
   ============================================================ */

function populateStationDropdowns(
    stations
) {

    const from =
        document.getElementById(
            "fromStation"
        );


    const to =
        document.getElementById(
            "toStation"
        );


    /*
     * If journey page elements are missing,
     * simply stop.
     */

    if (!from || !to) {

        return;

    }


    from.innerHTML = `

        <option value="">
            Select starting station
        </option>

    `;


    to.innerHTML = `

        <option value="">
            Select destination station
        </option>

    `;


    stations.forEach(
        station => {

            const stationName =
                station.station_name;


            const option1 =
                document.createElement(
                    "option"
                );


            option1.value =
                stationName;


            option1.textContent =
                stationName;


            const option2 =
                document.createElement(
                    "option"
                );


            option2.value =
                stationName;


            option2.textContent =
                stationName;


            from.appendChild(
                option1
            );


            to.appendChild(
                option2
            );

        }
    );

}


/* ============================================================
   SWAP STATIONS
   ============================================================ */

function swapStations() {

    const from =
        document.getElementById(
            "fromStation"
        );


    const to =
        document.getElementById(
            "toStation"
        );


    if (!from || !to) {

        return;

    }


    const temp =
        from.value;


    from.value =
        to.value;


    to.value =
        temp;

}


/* ============================================================
   FIND TRAINS
   ============================================================ */

async function findTrains() {

    const fromElement =
        document.getElementById(
            "fromStation"
        );


    const toElement =
        document.getElementById(
            "toStation"
        );


    const dayElement =
        document.getElementById(
            "journeyDay"
        );


    const timeElement =
        document.getElementById(
            "journeyTime"
        );


    const message =
        document.getElementById(
            "journeyMessage"
        );


    const results =
        document.getElementById(
            "trainResults"
        );


    if (
        !fromElement ||
        !toElement ||
        !dayElement ||
        !timeElement ||
        !message ||
        !results
    ) {

        return;

    }


    const from =
        fromElement.value;


    const to =
        toElement.value;


    const day =
        dayElement.value;


    const time =
        timeElement.value;


    message.className =
        "message";


    message.textContent =
        "";


    if (!from || !to) {

        message.textContent =
            "Please select both stations.";


        message.classList.add(
            "error"
        );


        return;

    }


    if (from === to) {

        message.textContent =
            "Starting and destination stations cannot be the same.";


        message.classList.add(
            "error"
        );


        return;

    }


    results.innerHTML = `

        <div class="loading">
            Searching for trains...
        </div>

    `;


    try {

        const params =
            new URLSearchParams({

                from_station:
                    from,

                to_station:
                    to,

                day:
                    day,

                time:
                    time || "06:00"

            });


        const data =
            await apiFetch(
                `/find-trains?${params.toString()}`
            );


        displayTrainResults(
            data.results || []
        );


        if (
            data.results &&
            data.results.length
        ) {

            message.textContent =
                `${data.results.length} upcoming train(s) found.`;


            message.classList.add(
                "success"
            );

        } else {

            message.textContent =
                "No trains found for the selected time.";


            message.classList.add(
                "error"
            );

        }


    } catch (error) {

        console.error(
            "Find trains error:",
            error
        );


        results.innerHTML = `

            <div class="empty-state">

                <div>⚠</div>

                <h3>
                    Could not find trains
                </h3>

                <p>
                    ${escapeHTML(
                        error.message
                    )}
                </p>

            </div>

        `;


        message.textContent =
            "Unable to connect to TrackX backend.";


        message.classList.add(
            "error"
        );

    }

}


/* ============================================================
   DISPLAY SEARCH RESULTS
   ============================================================ */

function displayTrainResults(
    trains
) {

    const container =
        document.getElementById(
            "trainResults"
        );


    if (!container) {

        return;

    }


    if (!trains.length) {

        container.innerHTML = `

            <div class="empty-state">

                <div>🚆</div>

                <h3>
                    No trains available
                </h3>

                <p>
                    Try selecting a later time.
                </p>

            </div>

        `;


        return;

    }


    container.innerHTML = "";


    trains.forEach(train => {

        const card =
            document.createElement(
                "div"
            );


        card.className =
            "train-result";


        card.innerHTML = `

            <div class="result-time">

                ${escapeHTML(
                    train.departure_time ||
                    "--:--"
                )}

            </div>


            <div>

                <div class="train-name">

                    ${escapeHTML(
                        train.train_id ||
                        "TRAIN"
                    )}

                </div>


                <div class="route">

                    ${escapeHTML(
                        train.from_station ||
                        ""
                    )}

                    →

                    ${escapeHTML(
                        train.to_station ||
                        ""
                    )}

                </div>

            </div>


            <div>

                <div class="train-name">

                    ${escapeHTML(
                        train.fleet_type ||
                        "RUNNING"
                    )}

                </div>


                <div class="route">
                    Metro service
                </div>

            </div>


            <div>

                <span class="active-badge">

                    ${escapeHTML(
                        train.status ||
                        "ACTIVE"
                    )}

                </span>

            </div>

        `;


        container.appendChild(
            card
        );

    });

}


/* ============================================================
   TRAINS RUNNING
   ============================================================ */

async function loadRunningTrains() {

    const container =
        document.getElementById(
            "runningGrid"
        );


    if (!container) {

        return;

    }


    try {

        container.innerHTML = `

            <div class="loading">
                Loading train schedule...
            </div>

        `;


        const day =
            getCurrentDay();


        /*
         * IMPORTANT:
         *
         * The direction is sent directly
         * to the backend.
         */

        const endpoint =
            "/train-running?day=" +
            encodeURIComponent(day) +
            "&direction=" +
            encodeURIComponent(
                runningDirection
            );


        console.log(
            "Loading running trains:",
            endpoint
        );


        const data =
            await apiFetch(
                endpoint
            );


        const trains =
            Array.isArray(
                data.trains
            )

                ? data.trains

                : [];


        const runningCount =
            document.getElementById(
                "runningCount"
            );


        if (runningCount) {

            runningCount.textContent =
                data.total_departures ??
                trains.length;

        }


        /*
         * Display ALL departures.
         *
         * We do NOT slice.
         * We do NOT limit to 25.
         * We do NOT filter by time here.
         */

        renderRunningTrains(
            trains
        );


        /*
         * Home next departures.
         */

        updateNextDeparture(
            trains
        );


        updateNextTwoDepartures(
            trains
        );


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


        updateNextDeparture(
            []
        );


        updateNextTwoDepartures(
            []
        );

    }

}


/* ============================================================
   RENDER RUNNING TRAINS
   ============================================================ */

function renderRunningTrains(
    trains
) {

    const container =
        document.getElementById(
            "runningGrid"
        );


    if (!container) {

        return;

    }


    container.innerHTML = "";


    if (!trains.length) {

        container.innerHTML = `

            <div class="empty-state">

                <div>🚆</div>

                <h3>
                    No scheduled trains
                </h3>

                <p>
                    No departures are available.
                </p>

            </div>

        `;


        return;

    }


    /*
     * COPY before sorting so the original
     * API array is not modified.
     */

    const sortedTrains =
        [...trains].sort(
            (a, b) => {

                return (
                    timeToMinutesFrontend(
                        a.departure_time ||
                        a.next_departure
                    )
                    -
                    timeToMinutesFrontend(
                        b.departure_time ||
                        b.next_departure
                    )
                );

            }
        );


    /*
     * DISPLAY EVERY DEPARTURE
     */

    sortedTrains.forEach(
        (train, index) => {

            const card =
                document.createElement(
                    "div"
                );


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
                (
                    runningDirection ===
                    "ALUVA_TO_TRIPUNITHURA"

                        ? "Aluva"

                        : "Tripunithura Terminal"
                );


            const to =
                train.to_station ||
                (
                    runningDirection ===
                    "ALUVA_TO_TRIPUNITHURA"

                        ? "Tripunithura Terminal"

                        : "Aluva"
                );


            const fleet =
                train.fleet_type ||
                "RUNNING";


            const status =
                train.status ||
                "UPCOMING";


            let badgeClass =
                "train-badge";


            if (
                status ===
                "UPCOMING"
            ) {

                badgeClass =
                    "train-badge upcoming";

            }


            else if (
                status ===
                "ACTIVE"
            ) {

                badgeClass =
                    "train-badge active";

            }


            else if (
                status ===
                "COMPLETED"
            ) {

                badgeClass =
                    "train-badge completed";

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


            container.appendChild(
                card
            );

        }
    );

}


/* ============================================================
   UPCOMING TRAINS
   ============================================================ */

async function loadUpcomingTrains() {

    const container =
        document.getElementById(
            "upcomingList"
        );


    const dayElement =
        document.getElementById(
            "scheduleDay"
        );


    if (!container || !dayElement) {

        return;

    }


    const day =
        dayElement.value;


    try {

        container.innerHTML = `

            <div class="loading">
                Loading AI schedule...
            </div>

        `;


        /*
         * IMPORTANT:
         *
         * Do NOT generate or stop the schedule
         * at 12:00 here.
         *
         * Backend /schedule is the source
         * of the complete AI schedule.
         */

        const data =
            await apiFetch(
                `/schedule?day=${encodeURIComponent(day)}`
            );


        const schedule =
            Array.isArray(
                data.schedule
            )

                ? data.schedule

                : [];


        container.innerHTML = "";


        if (!schedule.length) {

            container.innerHTML = `

                <div class="empty-state">

                    <div>◷</div>

                    <h3>
                        No schedule available
                    </h3>

                    <p>
                        No schedule found for
                        ${escapeHTML(day)}.
                    </p>

                </div>

            `;


            return;

        }


        /*
         * SORT COMPLETE SCHEDULE
         */

        const sortedSchedule =
            [...schedule].sort(
                (a, b) => {

                    return (
                        timeToMinutesFrontend(
                            a.departure_time
                        )
                        -
                        timeToMinutesFrontend(
                            b.departure_time
                        )
                    );

                }
            );


        /*
         * DISPLAY ALL SCHEDULED DEPARTURES.
         *
         * There is intentionally NO:
         *
         * slice(0, 25)
         *
         * filter(time < 12:00)
         *
         * or any other artificial limit.
         */

        sortedSchedule.forEach(
            train => {

                const row =
                    document.createElement(
                        "div"
                    );


                row.className =
                    "schedule-row";


                const from =
                    train.from_station ||
                    "Aluva";


                const to =
                    train.to_station ||
                    "Tripunithura Terminal";


                row.innerHTML = `

                    <div class="schedule-time">

                        ${escapeHTML(
                            train.departure_time ||
                            "--:--"
                        )}

                    </div>


                    <div class="schedule-train">

                        ${escapeHTML(
                            train.train_id ||
                            train.train ||
                            "TRAIN"
                        )}

                    </div>


                    <div class="schedule-route">

                        ${escapeHTML(
                            from
                        )}

                    </div>


                    <div class="schedule-route">

                        →

                        ${escapeHTML(
                            to
                        )}

                    </div>


                    <div class="schedule-status">

                        ${escapeHTML(
                            train.status ||
                            "ACTIVE"
                        )}

                    </div>

                `;


                container.appendChild(
                    row
                );

            }
        );


        console.log(
            `Loaded ${sortedSchedule.length} scheduled departures for ${day}`
        );


    } catch (error) {

        console.error(
            "Failed to load upcoming schedule:",
            error
        );


        container.innerHTML = `

            <div class="empty-state">

                <div>⚠</div>

                <h3>
                    Schedule unavailable
                </h3>

                <p>
                    ${escapeHTML(
                        error.message
                    )}
                </p>

            </div>

        `;

    }

}


/* ============================================================
   NEXT DEPARTURE
   ============================================================ */

function updateNextDeparture(
    trains
) {

    const nextElement =
        document.getElementById(
            "nextDeparture"
        );


    const routeElement =
        document.getElementById(
            "nextDepartureRoute"
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


        if (routeElement) {

            routeElement.textContent =
                "Waiting for schedule...";

        }


        return;

    }


    const now =
        new Date();


    const currentMinutes =
        now.getHours() * 60 +
        now.getMinutes() +
        now.getSeconds() / 60;


    const sortedTrains =
        [...trains].sort(
            (a, b) => {

                return (
                    timeToMinutesFrontend(
                        a.departure_time ||
                        a.next_departure
                    )
                    -
                    timeToMinutesFrontend(
                        b.departure_time ||
                        b.next_departure
                    )
                );

            }
        );


    let nextTrain =
        null;


    for (
        const train of sortedTrains
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

            nextTrain =
                train;

            break;

        }

    }


    if (!nextTrain) {

        nextElement.textContent =
            "No more trains";


        if (routeElement) {

            routeElement.textContent =
                "No more trains today";

        }


        return;

    }


    nextElement.textContent =
        nextTrain.departure_time ||
        nextTrain.next_departure ||
        "--:--";


    if (routeElement) {

        routeElement.textContent =
            `${nextTrain.from_station || "Aluva"} → ${nextTrain.to_station || "Tripunithura Terminal"}`;

    }

}


/* ============================================================
   HOME — NEXT TWO DEPARTURES
   ============================================================ */

function updateNextTwoDepartures(
    trains
) {

    const departure1 =
        document.getElementById(
            "heroDeparture1"
        );


    const route1 =
        document.getElementById(
            "heroRoute1"
        );


    const departure2 =
        document.getElementById(
            "heroDeparture2"
        );


    const route2 =
        document.getElementById(
            "heroRoute2"
        );


    if (
        !departure1 ||
        !route1 ||
        !departure2 ||
        !route2
    ) {

        return;

    }


    if (
        !trains ||
        !trains.length
    ) {

        departure1.textContent =
            "--:--";


        route1.textContent =
            "No departure available";


        departure2.textContent =
            "--:--";


        route2.textContent =
            "No departure available";


        return;

    }


    const now =
        new Date();


    const currentMinutes =
        now.getHours() * 60 +
        now.getMinutes() +
        now.getSeconds() / 60;


    const upcoming =
        [...trains]

            .filter(train => {

                const departure =
                    train.departure_time ||
                    train.next_departure;


                if (!departure) {

                    return false;

                }


                return (
                    timeToMinutesFrontend(
                        departure
                    ) >
                    currentMinutes
                );

            })


            .sort((a, b) => {

                return (
                    timeToMinutesFrontend(
                        a.departure_time ||
                        a.next_departure
                    )
                    -
                    timeToMinutesFrontend(
                        b.departure_time ||
                        b.next_departure
                    )
                );

            });


    if (upcoming[0]) {

        const train =
            upcoming[0];


        departure1.textContent =
            train.departure_time ||
            train.next_departure ||
            "--:--";


        route1.textContent =
            `${train.from_station || "Aluva"} → ${train.to_station || "Tripunithura Terminal"}`;

    } else {

        departure1.textContent =
            "--:--";


        route1.textContent =
            "No more trains today";

    }


    if (upcoming[1]) {

        const train =
            upcoming[1];


        departure2.textContent =
            train.departure_time ||
            train.next_departure ||
            "--:--";


        route2.textContent =
            `${train.from_station || "Aluva"} → ${train.to_station || "Tripunithura Terminal"}`;

    } else {

        departure2.textContent =
            "--:--";


        route2.textContent =
            "No more trains today";

    }

}


/* ============================================================
   TIME CONVERTER
   ============================================================ */

function timeToMinutesFrontend(
    value
) {

    if (!value) {

        return 0;

    }


    const parts =
        String(value).split(":");


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
   LIVE REFRESH
   ============================================================ */

function startNextDepartureTimer() {

    /*
     * Refresh every 30 seconds.
     *
     * This does NOT change the AI schedule.
     * It only refreshes live status and next departures.
     */

    setInterval(
        async function () {

            try {

                const day =
                    getCurrentDay();


                const endpoint =
                    "/train-running?day=" +
                    encodeURIComponent(day) +
                    "&direction=" +
                    encodeURIComponent(
                        runningDirection
                    );


                const data =
                    await apiFetch(
                        endpoint
                    );


                const trains =
                    Array.isArray(
                        data.trains
                    )

                        ? data.trains

                        : [];


                updateNextDeparture(
                    trains
                );


                updateNextTwoDepartures(
                    trains
                );


                /*
                 * If user is viewing
                 * Trains Running,
                 * refresh the cards.
                 */

                const runningSection =
                    document.getElementById(
                        "running"
                    );


                if (
                    runningSection &&
                    runningSection.classList.contains(
                        "active-section"
                    )
                ) {

                    renderRunningTrains(
                        trains
                    );


                    const count =
                        document.getElementById(
                            "runningCount"
                        );


                    if (count) {

                        count.textContent =
                            data.total_departures ??
                            trains.length;

                    }

                }


            } catch (error) {

                console.error(
                    "Running train update failed:",
                    error
                );

            }

        },
        30000
    );

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


    return days[
        new Date().getDay()
    ];

}


function setupCurrentDay() {

    const day =
        getCurrentDay();


    const currentDay =
        document.getElementById(
            "currentDay"
        );


    const journeyDay =
        document.getElementById(
            "journeyDay"
        );


    const scheduleDay =
        document.getElementById(
            "scheduleDay"
        );


    if (currentDay) {

        currentDay.textContent =
            day;

    }


    if (journeyDay) {

        journeyDay.value =
            day;

    }


    if (scheduleDay) {

        scheduleDay.value =
            day;

    }

}


/* ============================================================
   BACKEND STATUS
   ============================================================ */

async function checkBackend() {

    const status =
        document.getElementById(
            "backendStatus"
        );


    try {

        const data =
            await apiFetch("/");


        console.log(
            "TrackX backend connected:",
            data
        );


        if (status) {

            status.className =
                "backend-status online";


            status.innerHTML = `

                <span class="status-dot"></span>

                TRACKX SYSTEM ONLINE

            `;

        }


        return true;


    } catch (error) {

        console.error(
            "Backend connection failed:",
            error
        );


        if (status) {

            status.className =
                "backend-status offline";


            status.innerHTML = `

                <span class="status-dot"></span>

                BACKEND OFFLINE

            `;

        }


        return false;

    }

}


/* ============================================================
   ESCAPE HTML
   ============================================================ */

function escapeHTML(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";

    }


    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );

}


/* ============================================================
   INITIALIZE TRACKX
   ============================================================ */

async function initializeTrackX() {

    console.log(
        "Initializing TrackX..."
    );


    /*
     * Set day first.
     */

    setupCurrentDay();


    /*
     * Set default direction WITHOUT
     * depending on backend.
     */

    runningDirection =
        "ALUVA_TO_TRIPUNITHURA";


    const outboundBtn =
        document.getElementById(
            "outboundRunningBtn"
        );


    const returnBtn =
        document.getElementById(
            "returnRunningBtn"
        );


    if (outboundBtn) {

        outboundBtn.classList.add(
            "active"
        );

    }


    if (returnBtn) {

        returnBtn.classList.remove(
            "active"
        );

    }


    /*
     * Check backend.
     */

    await checkBackend();


    /*
     * Load stations.
     *
     * IMPORTANT:
     * loadStations() is now safe even though
     * stationGrid is missing from your HTML.
     */

    await loadStations();


    /*
     * Load running trains.
     */

    await loadRunningTrains();


    /*
     * Start live updates.
     */

    startNextDepartureTimer();


    console.log(
        "TrackX initialization complete."
    );

}


/* ============================================================
   START APPLICATION
   ============================================================ */

document.addEventListener(
    "DOMContentLoaded",
    initializeTrackX
);