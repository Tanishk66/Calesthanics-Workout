let workouts = JSON.parse(localStorage.getItem('workouts')) || [];
let currentWorkout = null;
let currentExerciseIndex = 0;
let countdown = 10;
let timerInterval;
let stopwatchInterval, stopwatchSeconds = 0;

// 🌙 Dark Mode Toggle
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// 📜 Toggle Workout List Animation (☰ Menu)
function toggleWorkoutList() {
    let workoutList = document.getElementById('workout-list');
    workoutList.classList.toggle('show');
    loadWorkoutList();
}

// 🏋️ Add Workout
function addWorkout() {
    openSlide('add-workout');
    document.getElementById('workout-name-input').value = '';
    document.getElementById('exercise-list').innerHTML = '';
}

// ➕ Add Exercise
function addExercise() {
    let exerciseName = prompt('Enter Exercise Name 🏋️:');
    let exerciseTime = prompt('Enter Exercise Time (seconds) ⏳:');

    if (exerciseName && exerciseTime) {
        let exerciseList = document.getElementById('exercise-list');
        let exerciseItem = document.createElement('p');
        exerciseItem.innerHTML = `🏋️ ${exerciseName} - ⏳ ${exerciseTime}s`;
        exerciseList.appendChild(exerciseItem);
    }
}

// 💾 Save Workout
function saveWorkout() {
    let workoutName = document.getElementById('workout-name-input').value;
    let exercises = [...document.querySelectorAll('#exercise-list p')].map(ex => {
        let parts = ex.innerText.split(' - ');
        return { name: parts[0].replace('🏋️ ', ''), time: parseInt(parts[1].replace('⏳ ', '')) };
    });

    if (workoutName && exercises.length > 0) {
        workouts.push({ name: workoutName, exercises });
        localStorage.setItem('workouts', JSON.stringify(workouts));
        goHome();
    } else {
        alert('Please enter a workout name and at least one exercise!');
    }
}

// 📜 Toggle Workout List Animation (☰ Menu)
function toggleWorkoutList() {
    let workoutList = document.getElementById('workout-list');
    workoutList.classList.toggle('show');
    loadWorkoutList();
}

// 📋 Load Workouts into Sidebar (☰ Menu)
function loadWorkoutList() {
    let container = document.getElementById('workout-container');
    container.innerHTML = '';

    if (workouts.length === 0) {
        container.innerHTML = "<p class='no-data'>❌ No saved workouts available!</p>";
        return;
    }

    workouts.forEach((workout, index) => {
        let workoutItem = document.createElement('div');
        workoutItem.classList.add('workout-item');
        workoutItem.innerHTML = `<span>${workout.name}</span>`;
        workoutItem.onclick = () => startWorkout(index);
        container.appendChild(workoutItem);
    });
}

// 🗑️ Delete Workout (Shows List or "No Workouts" Message)
function deleteWorkout() {
    openSlide('delete-workout');
    let deleteContainer = document.getElementById('workout-checkboxes');
    deleteContainer.innerHTML = '';

    if (workouts.length === 0) {
        deleteContainer.innerHTML = "<p class='no-data'>❌ No workouts available to delete!</p>";
        return;
    }

    workouts.forEach((workout, index) => {
        let div = document.createElement('div');
        div.innerHTML = `
            <input type="checkbox" id="workout-${index}" />
            <label for="workout-${index}">${workout.name}</label>
        `;
        deleteContainer.appendChild(div);
    });
}

// ✅ Confirm Workout Deletion
function confirmDelete() {
    let checkboxes = document.querySelectorAll('#workout-checkboxes input[type="checkbox"]');
    let newWorkouts = workouts.filter((_, index) => !checkboxes[index].checked);

    if (newWorkouts.length !== workouts.length) {
        workouts = newWorkouts;
        localStorage.setItem('workouts', JSON.stringify(workouts));
        alert("✅ Selected Workouts Deleted!");
    }
    goHome();
}


// 🚀 Start Selected Workout
function startWorkout(index) {
    currentWorkout = workouts[index];
    currentExerciseIndex = 0;
    openSlide('start-workout');
    startCountdown();
}

// ⏳ 10-Second Countdown Before Workout
function startCountdown() {
    let timerDisplay = document.getElementById('timer');
    timerDisplay.innerText = `⏳ ${countdown}`;
    timerInterval = setInterval(() => {
        countdown--;
        timerDisplay.innerText = `⏳ ${countdown}`;
        if (countdown === 0) {
            clearInterval(timerInterval);
            startExercise();
        }
    }, 1000);
}

// 🏋️ Start Each Exercise
function startExercise() {
    if (currentExerciseIndex < currentWorkout.exercises.length) {
        let exercise = currentWorkout.exercises[currentExerciseIndex];
        document.getElementById('exercise-display').innerText = `🏋️ ${exercise.name} - ⏳ ${exercise.time}s`;
        countdown = exercise.time;
        timerInterval = setInterval(() => {
            countdown--;
            document.getElementById('timer').innerText = `⏳ ${countdown}`;
            if (countdown === 0) {
                clearInterval(timerInterval);
                currentExerciseIndex++;
                startExercise();
            }
        }, 1000);
    } else {
        endWorkout();
    }
}

// ⏸️ Pause/Resume Workout
function pauseResume() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    } else {
        startExercise();
    }
}

// ⏩ Skip to Next Exercise
function nextExercise() {
    clearInterval(timerInterval);
    currentExerciseIndex++;
    startExercise();
}

// 🎉 End of Workout Message
function endWorkout() {
    alert("🎉 Great Work! Exercise Done!");
    goHome();
}

// ⏱️ Stopwatch Functions (Fixed!)
function startStopwatch() {
    clearInterval(stopwatchInterval);
    stopwatchInterval = setInterval(() => {
        stopwatchSeconds++;
        document.getElementById('stopwatch-display').innerText = formatTime(stopwatchSeconds);
    }, 1000);
}

function pauseStopwatch() {
    clearInterval(stopwatchInterval);
}

function resetStopwatch() {
    clearInterval(stopwatchInterval);
    stopwatchSeconds = 0;
    document.getElementById('stopwatch-display').innerText = "00:00:00";
}

// 🔄 Slide Navigation
function openSlide(id) {
    document.querySelectorAll('.slide').forEach(slide => slide.classList.add('hidden'));
    document.getElementById(id).classList.remove('hidden');
}

function goHome() {
    openSlide('home');
    loadWorkoutList();
}

// 📌 Format Time for Stopwatch
function formatTime(seconds) {
    let h = Math.floor(seconds / 3600);
    let m = Math.floor((seconds % 3600) / 60);
    let s = seconds % 60;
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}