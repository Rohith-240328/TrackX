const API_URL ="https://trackx-backend-nf6f.onrender.com";

let employeeToken = null;


/* ============================================================
   INITIALIZATION
   ============================================================ */

document.addEventListener(
    "DOMContentLoaded",
    initializeEmployee
);


async function initializeEmployee() {

    console.log("TRACKX EMPLOYEE FRONTEND");
    console.log("API:", API_URL);

    updateDay();

    await checkBackend();

    const savedToken =
        sessionStorage.getItem("trackx_employee_token");

   if (savedToken) {

    employeeToken = savedToken;

    showDashboard();

    await refreshAll();

    setInterval(
        loadOperationalAnalytics,
        30000
    );

}
}


/* ============================================================
   DAY
   ============================================================ */

function updateDay() {

    const days = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ];

    const day =
        days[new Date().getDay()];

    const element =
        document.getElementById("currentDay");

    if (element) {
        element.textContent = day;
    }

    const scheduleDay =
        document.getElementById("scheduleDay");

    if (scheduleDay) {
        scheduleDay.value = day;
    }
}


/* ============================================================
   BACKEND CHECK
   ============================================================ */

async function checkBackend() {

    const status =
        document.getElementById("backendStatus");

    try {

        const response =
            await fetch(API_URL + "/");

        if (!response.ok) {
            throw new Error("Backend error");
        }

        const data =
            await response.json();

        console.log(
            "BACKEND ONLINE:",
            data
        );

        status.className =
            "backend-status online";

        status.textContent =
            "● BACKEND ONLINE";

        return true;

    } catch (error) {

        console.error(
            "BACKEND OFFLINE:",
            error
        );

        status.className =
            "backend-status offline";

        status.textContent =
            "● BACKEND OFFLINE";

        return false;
    }
}


/* ============================================================
   API HELPER
   ============================================================ */

async function apiFetch(
    endpoint,
    options = {}
) {

    const headers = {
        ...(options.headers || {})
    };

    if (employeeToken) {
        headers["Authorization"] =
            `Bearer ${employeeToken}`;
    }

    const response =
        await fetch(
            API_URL + endpoint,
            {
                ...options,
                headers
            }
        );

    if (!response.ok) {

        let message =
            `HTTP ${response.status}`;

        try {

            const data =
                await response.json();

            if (data.detail) {
                message = data.detail;
            }

        } catch (error) {}

        throw new Error(message);
    }

    return await response.json();
}


/* ============================================================
   LOGIN
   ============================================================ */

async function loginEmployee() {

    const employeeId =
        document.getElementById(
            "employeeId"
        ).value.trim();

    const password =
        document.getElementById(
            "employeePassword"
        ).value;

    const message =
        document.getElementById(
            "loginMessage"
        );

    message.textContent = "";

    if (!employeeId || !password) {

        message.textContent =
            "Enter Employee ID and password.";

        return;
    }

    try {

        const response =
            await fetch(
                API_URL + "/employee/login",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        employee_id:
                            employeeId,

                        password:
                            password
                    })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail ||
                "Login failed."
            );
        }

        employeeToken =
            data.token;

        sessionStorage.setItem(
            "trackx_employee_token",
            employeeToken
        );

        showDashboard();

        await refreshAll();

    } catch (error) {

        console.error(error);

        message.textContent =
            error.message;
    }
}


/* ============================================================
   SHOW DASHBOARD
   ============================================================ */

function showDashboard() {

    document.getElementById(
        "loginSection"
    ).classList.add("hidden");

    document.getElementById(
        "dashboard"
    ).classList.remove("hidden");
}


/* ============================================================
   LOGOUT
   ============================================================ */

function logout() {

    employeeToken = null;

    sessionStorage.removeItem(
        "trackx_employee_token"
    );

    document.getElementById(
        "dashboard"
    ).classList.add("hidden");

    document.getElementById(
        "loginSection"
    ).classList.remove("hidden");
}


/* ============================================================
   REFRESH EVERYTHING
   ============================================================ */

async function refreshAll() {

    if (!employeeToken) {
        return;
    }

   await Promise.all([
    loadFleet(),
    loadStations(),
    loadSchedule(),
    loadOperationalAnalytics()
]);
}


/* ============================================================
   LOAD FLEET
   ============================================================ */

async function loadFleet() {

    try {

        const data =
            await apiFetch(
                "/employee/trains"
            );

        console.log(
            "FLEET DATA:",
            data
        );

        updateFleetSummary(data);

        renderAvailable(
            data.available_trains || []
        );

        renderUnavailable(
            data.unavailable_trains || []
        );

        renderBackups(
            data.backup_trains || []
        );

    } catch (error) {

        console.error(
            "Fleet loading error:",
            error
        );

        document.getElementById(
            "availableTrains"
        ).innerHTML =
            `<div class="empty">
                Unable to load fleet.
                ${escapeHTML(error.message)}
            </div>`;
    }
}


/* ============================================================
   SUMMARY
   ============================================================ */

function updateFleetSummary(data) {

    document.getElementById(
        "totalTrains"
    ).textContent =
        data.total_trains ?? 0;

    document.getElementById(
        "availableCount"
    ).textContent =
        data.available_count ?? 0;

    document.getElementById(
        "unavailableCount"
    ).textContent =
        data.unavailable_count ?? 0;

    document.getElementById(
        "backupCount"
    ).textContent =
        data.backup_count ?? 0;

    document.getElementById(
        "availableColumnCount"
    ).textContent =
        data.available_count ?? 0;

    document.getElementById(
        "unavailableColumnCount"
    ).textContent =
        data.unavailable_count ?? 0;
}


/* ============================================================
   AVAILABLE TRAINS
   ============================================================ */

function renderAvailable(trains) {

    const container =
        document.getElementById(
            "availableTrains"
        );

    container.innerHTML = "";

    if (!trains.length) {

        container.innerHTML =
            `<div class="empty">
                No available trains.
            </div>`;

        return;
    }

    trains.forEach(train => {

        const item =
            document.createElement("div");

        item.className =
            "train-item";

        item.innerHTML = `

            <div class="train-info">

                <strong>
                    ${escapeHTML(
                        train.train_id
                    )}
                </strong>

                <span>
                    READY FOR SERVICE
                </span>

            </div>

            <button
                class="train-action unavailable"
                onclick="setTrainAvailability(
                    '${escapeJS(train.train_id)}',
                    false
                )">

                Mark Unavailable

            </button>

        `;

        container.appendChild(item);
    });
}


/* ============================================================
   UNAVAILABLE TRAINS
   ============================================================ */

function renderUnavailable(trains) {

    const container =
        document.getElementById(
            "unavailableTrains"
        );

    container.innerHTML = "";

    if (!trains.length) {

        container.innerHTML =
            `<div class="empty">
                No unavailable trains.
            </div>`;

        return;
    }

    trains.forEach(train => {

        const item =
            document.createElement("div");

        item.className =
            "train-item";

        item.innerHTML = `

            <div class="train-info">

                <strong>
                    ${escapeHTML(
                        train.train_id
                    )}
                </strong>

                <span>
                    NOT AVAILABLE
                </span>

            </div>

            <button
                class="train-action restore"
                onclick="setTrainAvailability(
                    '${escapeJS(train.train_id)}',
                    true
                )">

                Make Available

            </button>

        `;

        container.appendChild(item);
    });
}


/* ============================================================
   UPDATE TRAIN AVAILABILITY
   ============================================================ */

async function setTrainAvailability(
    trainId,
    available
) {

    const action =
        available
            ? "restore"
            : "mark unavailable";

    if (
        !confirm(
            `Are you sure you want to ${action} ${trainId}?`
        )
    ) {
        return;
    }

    try {

        /*
         * THIS IS THE CORRECT BACKEND ENDPOINT.
         *
         * POST:
         * /employee/trains/{train_id}/availability
         */

        const data =
            await apiFetch(
                `/employee/trains/${encodeURIComponent(
                    trainId
                )}/availability`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        available:
                            available
                    })
                }
            );

        console.log(
            "TRAIN UPDATED:",
            data
        );

        await loadFleet();

    } catch (error) {

        console.error(
            "Train availability update failed:",
            error
        );

        alert(
            "Unable to update train.\n\n" +
            error.message
        );
    }
}


/* ============================================================
   BACKUP TRAINS
   ============================================================ */

function renderBackups(trains) {

    const container =
        document.getElementById(
            "backupTrains"
        );

    container.innerHTML = "";

    if (!trains.length) {

        container.innerHTML =
            `<div class="empty">
                No backup trains.
            </div>`;

        return;
    }

    trains.forEach(train => {

        const card =
            document.createElement("div");

        card.className =
            "backup-card" +
            (
                train.in_service
                    ? " assigned"
                    : ""
            );

        let statusText =
            "AVAILABLE AS BACKUP";

        if (train.in_service) {

            statusText =
                "REPLACING " +
                (train.assigned_to || "TRAIN");
        }

        card.innerHTML = `

            <strong>
                ${escapeHTML(
                    train.train_id
                )}
            </strong>

            <span>
                ${escapeHTML(statusText)}
            </span>
        `;

        container.appendChild(card);
    });
}


/* ============================================================
   STATIONS
   ============================================================ */

async function loadStations() {

    const container =
        document.getElementById(
            "stations"
        );

    try {

        const stations =
            await apiFetch(
                "/stations"
            );

        container.innerHTML = "";

        stations.forEach(
            (station, index) => {

                const card =
                    document.createElement("div");

                card.className =
                    "station-card";

                card.innerHTML = `

                    <div class="station-number">
                        STATION
                        ${String(
                            index + 1
                        ).padStart(2, "0")}
                    </div>

                    <strong>
                        ${escapeHTML(
                            station.station_name
                        )}
                    </strong>
                `;

                container.appendChild(card);
            }
        );

    } catch (error) {

        container.innerHTML =
            `<div class="empty">
                Unable to load stations.
            </div>`;

        console.error(error);
    }
}


/* ============================================================
   AI SCHEDULE
   ============================================================ */

async function loadSchedule() {

    const container =
        document.getElementById(
            "schedule"
        );

    const day =
        document.getElementById(
            "scheduleDay"
        ).value;

    try {

        container.innerHTML =
            `<div class="loading">
                Loading AI schedule...
            </div>`;

        const data =
            await apiFetch(
                `/employee/schedule?day=${encodeURIComponent(
                    day
                )}`
            );

        const schedule =
            data.schedule || [];

        container.innerHTML = "";

        if (!schedule.length) {

            container.innerHTML =
                `<div class="empty">
                    No schedule available.
                </div>`;

            return;
        }

        /*
         * SHOW COMPLETE SCHEDULE.
         *
         * There is deliberately NO slice(0, 50).
         */

        schedule.forEach(train => {

            const row =
                document.createElement("div");

            row.className =
                "schedule-row";

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
                        "NO TRAIN"
                    )}
                </div>

                <div class="schedule-route">
                    ${escapeHTML(
                        train.from_station ||
                        "Aluva"
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
                        train.status ||
                        "ACTIVE"
                    )}
                </div>

            `;

            container.appendChild(row);
        });

    } catch (error) {

        container.innerHTML =
            `<div class="empty">
                Unable to load AI schedule.
                ${escapeHTML(error.message)}
            </div>`;

        console.error(error);
    }
}
/* ============================================================
   OPERATIONAL ANALYTICS
   LIVE DEPARTURE + FLEET STATUS
   ============================================================ */

async function loadOperationalAnalytics() {

    try {

        const day =
            document.getElementById("scheduleDay")?.value ||
            getCurrentDayEmployee();


        /* ----------------------------------------------------
           GET COMPLETE DAILY SCHEDULE
           ---------------------------------------------------- */

        const scheduleData =
            await apiFetch(
                `/employee/schedule?day=${encodeURIComponent(day)}`
            );


        const schedule =
            Array.isArray(scheduleData.schedule)
                ? scheduleData.schedule
                : [];


        /* ----------------------------------------------------
           TOTAL SCHEDULED DEPARTURES
           ---------------------------------------------------- */

        const totalDepartures =
            schedule.length;


        /* ----------------------------------------------------
           CURRENT TIME
           ---------------------------------------------------- */

        const now =
            new Date();


        const currentMinutes =
            now.getHours() * 60 +
            now.getMinutes() +
            now.getSeconds() / 60;


        /* ----------------------------------------------------
           COMPLETED DEPARTURES

           A departure becomes COMPLETED when its
           departure time has passed.
           ---------------------------------------------------- */

        let completedDepartures = 0;


        schedule.forEach(train => {

            const departure =
                train.departure_time;


            if (!departure) {
                return;
            }


            const departureMinutes =
                employeeTimeToMinutes(
                    departure
                );


            if (
                departureMinutes <=
                currentMinutes
            ) {

                completedDepartures++;

            }

        });


        /* ----------------------------------------------------
           UPCOMING DEPARTURES
           ---------------------------------------------------- */

        const upcomingDepartures =
            Math.max(
                0,
                totalDepartures -
                completedDepartures
            );


        /* ----------------------------------------------------
           GET CURRENT FLEET STATUS
           ---------------------------------------------------- */

        const fleetData =
            await apiFetch(
                "/employee/trains"
            );


        /*
         * Total operational fleet:
         *
         * TRAIN-01 → TRAIN-25
         */

        const totalRunningFleet = 25;


        /*
         * Backup fleet:
         *
         * TRAIN-26 → TRAIN-30
         */

        const totalBackupFleet = 5;


        /*
         * Available running trains.
         *
         * The backend's available_count includes
         * the currently available operational trains.
         */

        const availableRunning =
            Math.min(
                totalRunningFleet,
                fleetData.available_count ?? 0
            );


        /*
         * Backup trains currently available.
         */

        const backupAvailable =
            Math.min(
                totalBackupFleet,
                fleetData.backup_count ?? 0
            );


        /* ----------------------------------------------------
           UPDATE UI
           ---------------------------------------------------- */

        setAnalyticsValue(
            "totalScheduledDepartures",
            totalDepartures
        );


        setAnalyticsValue(
            "completedDepartures",
            completedDepartures
        );


        setAnalyticsValue(
            "upcomingDepartures",
            upcomingDepartures
        );


        setAnalyticsValue(
            "runningFleet",
            `${availableRunning} / ${totalRunningFleet}`
        );


        setAnalyticsValue(
            "backupFleet",
            `${backupAvailable} / ${totalBackupFleet}`
        );


        console.log(
            "OPERATIONAL ANALYTICS:",
            {
                day,
                totalDepartures,
                completedDepartures,
                upcomingDepartures,
                runningFleet:
                    `${availableRunning} / ${totalRunningFleet}`,
                backupFleet:
                    `${backupAvailable} / ${totalBackupFleet}`
            }
        );


    } catch (error) {

        console.error(
            "Operational analytics error:",
            error
        );

    }

}


/* ============================================================
   ANALYTICS VALUE HELPER
   ============================================================ */

function setAnalyticsValue(
    elementId,
    value
) {

    const element =
        document.getElementById(
            elementId
        );


    if (element) {

        element.textContent =
            value;

    }

}


/* ============================================================
   EMPLOYEE TIME CONVERTER
   ============================================================ */

function employeeTimeToMinutes(
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
   CURRENT DAY
   ============================================================ */

function getCurrentDayEmployee() {

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


/* ============================================================
   ESCAPE HTML
   ============================================================ */

function escapeHTML(value) {

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
   ESCAPE JAVASCRIPT
   ============================================================ */

function escapeJS(value) {

    return String(value)
        .replace(
            /\\/g,
            "\\\\"
        )
        .replace(
            /'/g,
            "\\'"
        );
}