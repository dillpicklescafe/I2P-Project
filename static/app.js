const goalSelect = document.querySelector("#goal");
const goalPicker = document.querySelector(".goal-picker");
const goalTrigger = document.querySelector("#goal-trigger");
const goalPopover = document.querySelector("#goal-popover");
const goalOptions = document.querySelector("#goal-options");
const goalSelected = document.querySelector("#goal-selected");
const durationSelect = document.querySelector("#duration");
const equipmentOptions = document.querySelector("#equipment-options");
const recommendButton = document.querySelector("#recommend-button");
const plannerMessage = document.querySelector("#planner-message");
const workoutSection = document.querySelector("#workout-section");
const exerciseList = document.querySelector("#exercise-list");
const completionCount = document.querySelector("#completion-count");
const savePanel = document.querySelector("#save-panel");
const saveButton = document.querySelector("#save-button");
const saveMessage = document.querySelector("#save-message");
const historyList = document.querySelector("#history-list");
const historyMessage = document.querySelector("#history-message");
const authSection = document.querySelector("#auth-section");
const authForm = document.querySelector("#auth-form");
const authMessage = document.querySelector("#auth-message");
const authSubmit = document.querySelector("#auth-submit");
const signupNameFields = document.querySelector("#signup-name-fields");
const authFirstName = document.querySelector("#auth-first-name");
const authLastName = document.querySelector("#auth-last-name");
const authPassword = document.querySelector("#auth-password");
const passwordHint = document.querySelector("#password-hint");
const authSwitchCopy = document.querySelector("#auth-switch-copy");
const authSwitchLink = document.querySelector("#auth-switch-link");
const logoutButton = document.querySelector("#logout-button");
const appContent = document.querySelector("#app-content");
const welcomeName = document.querySelector("#welcome-name");
const appNav = document.querySelector("#app-nav");
let currentGoal = "";
let workoutSaved = false;
let authMode = "login";

const equipmentIcons = {
  bar: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M7 11v10M11 8v16M21 8v16M25 11v10M11 16h10"/></svg>',
  bench: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M5 13h22v5H5zM9 18v8M23 18v8"/></svg>',
  chair: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M9 7v11h16v-7H9M11 18v8M23 18v8M9 12H6v8h20"/></svg>',
  dumbbells: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M4 12v8M8 9v14M24 9v14M28 12v8M8 16h16"/></svg>',
  resistance_band: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M7 23C7 8 25 8 25 23M7 23h5m8 0h5"/></svg>',
  step: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M5 23h8v-6h7v-6h7M5 23v4h22v-4"/></svg>',
  wall: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M7 6h18v20H7zM7 13h18M7 20h18M13 6v7m7 0v7m-7 0v6"/></svg>',
};

function makeElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

function prettyLabel(value) {
  return value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function renderGoalCard(goal) {
  const card = makeElement("button", "goal-card");
  card.type = "button";
  card.dataset.goal = goal;
  card.setAttribute("aria-pressed", "false");

  const image = makeElement("span", "goal-image-placeholder");
  image.setAttribute("role", "img");
  image.setAttribute("aria-label", `${prettyLabel(goal)} image placeholder`);
  image.innerHTML = '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="15"/><circle cx="24" cy="24" r="8"/><circle cx="24" cy="24" r="2"/><path d="m32 16 8-8m-5 0h5v5"/></svg><span>Image soon</span>';
  card.append(image, makeElement("span", "goal-card-label", prettyLabel(goal)));
  card.addEventListener("click", () => selectGoal(goal));
  return card;
}

function renderEquipmentOption(item) {
  const label = makeElement("label", "equipment-chip");
  const checkbox = makeElement("input");
  checkbox.type = "checkbox";
  checkbox.name = "equipment";
  checkbox.value = item;

  const content = makeElement("span", "equipment-chip-content");
  const icon = makeElement("span", "equipment-icon");
  icon.innerHTML = equipmentIcons[item] || equipmentIcons.bar;
  content.append(icon, makeElement("span", "equipment-name", prettyLabel(item)));
  label.append(checkbox, content);
  return label;
}

function setGoalPickerOpen(open) {
  goalPopover.hidden = !open;
  goalTrigger.setAttribute("aria-expanded", String(open));
}

function selectGoal(goal) {
  goalSelect.value = goal;
  goalSelected.textContent = prettyLabel(goal);
  goalOptions.querySelectorAll(".goal-card").forEach((card) => {
    const selected = card.dataset.goal === goal;
    card.classList.toggle("is-selected", selected);
    card.setAttribute("aria-pressed", String(selected));
  });
  plannerMessage.textContent = "";
  recommendButton.disabled = false;
  setGoalPickerOpen(false);
}

async function requestJson(url, options) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Something went wrong. Please try again.");
  return data;
}

function updateCompletion() {
  const checkboxes = [...exerciseList.querySelectorAll(".complete-toggle input")];
  const completed = checkboxes.filter((checkbox) => checkbox.checked).length;
  completionCount.textContent = `${completed} / ${checkboxes.length} complete`;
  savePanel.hidden = checkboxes.length === 0;
  saveButton.disabled = completed === 0 || workoutSaved;
  checkboxes.forEach((checkbox) => {
    checkbox.closest(".exercise-card").classList.toggle("is-complete", checkbox.checked);
  });
}

function renderExercise(exercise) {
  const card = makeElement("article", "exercise-card");
  if (exercise.media_url && exercise.media_type === "mp4") {
    const video = makeElement("video", "exercise-media");
    video.controls = true;
    video.muted = true;
    video.loop = true;
    video.playsInline = true;
    const source = makeElement("source");
    source.src = exercise.media_url;
    source.type = "video/mp4";
    video.append(source);
    card.append(video);
  } else if (exercise.media_url) {
    const image = makeElement("img", "exercise-media");
    image.src = exercise.media_url;
    image.alt = `${exercise.name} demonstration`;
    card.append(image);
  } else {
    card.append(makeElement("div", "media-placeholder", "Demo coming soon"));
  }

  const content = makeElement("div", "exercise-content");
  const heading = makeElement("div", "exercise-top");
  heading.append(makeElement("h3", "exercise-title", exercise.name));
  heading.append(makeElement("span", "exercise-time", `~${exercise.duration} min`));
  content.append(heading);

  const meta = makeElement("div", "exercise-meta");
  let prescription = `${exercise.sets} sets`;
  if (exercise.reps !== null) prescription += ` × ${exercise.reps} reps`;
  else if (exercise.hold_seconds !== null) prescription += ` × ${exercise.hold_seconds}s hold`;
  else if (exercise.work_seconds !== null) prescription += ` × ${exercise.work_seconds}s work`;
  meta.append(makeElement("span", "meta-pill", prescription));
  if (exercise.work_seconds !== null && exercise.rest_seconds !== null) {
    meta.append(makeElement("span", "meta-pill", `${exercise.rest_seconds}s rest between sets`));
  }
  content.append(meta);

  const instructions = makeElement("ol");
  exercise.instructions.forEach((instruction) => instructions.append(makeElement("li", "", instruction)));
  content.append(instructions);

  const bottom = makeElement("div", "exercise-bottom");
  const equipment = makeElement("div", "equipment-tags");
  if (exercise.equipment.length) {
    exercise.equipment.forEach((item) => equipment.append(makeElement("span", "equipment-tag", prettyLabel(item))));
  } else {
    equipment.append(makeElement("span", "equipment-tag", "No equipment"));
  }
  bottom.append(equipment);

  const toggleLabel = makeElement("label", "complete-toggle");
  const checkbox = makeElement("input");
  checkbox.type = "checkbox";
  checkbox.value = String(exercise.id);
  checkbox.addEventListener("change", updateCompletion);
  toggleLabel.append(checkbox, makeElement("span", "", "Done"));
  bottom.append(toggleLabel);
  content.append(bottom);
  card.append(content);
  return card;
}

function renderRecommendations(exercises, goal, duration) {
  workoutSaved = false;
  currentGoal = goal;
  exerciseList.replaceChildren(...exercises.map(renderExercise));
  document.querySelector("#workout-summary").textContent =
    `${prettyLabel(goal)} · ${prettyLabel(document.querySelector('input[name="level"]:checked').value)} · up to ${duration} minutes`;
  document.querySelector("#no-results").hidden = exercises.length !== 0;
  savePanel.hidden = exercises.length === 0;
  workoutSection.hidden = false;
  saveMessage.textContent = "";
  saveMessage.className = "status-message";
  updateCompletion();
  workoutSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderHistory(history) {
  if (history.length === 0) {
    historyList.replaceChildren(makeElement("p", "history-empty", "Your saved workouts will show up here."));
    return;
  }

  historyList.replaceChildren(...history.map((workout) => {
    const card = makeElement("article", "history-card");
    const main = makeElement("div", "history-main");
    const summary = makeElement("div");
    const date = new Date(workout.date);
    summary.append(makeElement("p", "history-date", Number.isNaN(date.getTime()) ? workout.date : date.toLocaleString()));
    summary.append(makeElement(
      "p",
      "history-detail",
      `${workout.total_exercises} exercises · ${workout.total_sets} sets · ${workout.total_duration} min`
    ));
    main.append(summary, makeElement("span", "history-goal", prettyLabel(workout.goal || "workout")));
    card.append(main);

    const button = makeElement("button", "history-expand", "View exercises +");
    button.type = "button";
    button.setAttribute("aria-expanded", "false");
    button.addEventListener("click", async () => {
      const existing = card.querySelector(".history-exercises");
      if (existing) {
        existing.remove();
        button.textContent = "View exercises +";
        button.setAttribute("aria-expanded", "false");
        return;
      }

      button.disabled = true;
      try {
        const detail = await requestJson(`/api/history/${encodeURIComponent(workout.session_id)}`);
        const list = makeElement("ul", "history-exercises");
        detail.exercises.forEach((exercise) => {
          const reps = exercise.reps_completed === null ? "" : ` × ${exercise.reps_completed} reps`;
          list.append(makeElement(
            "li",
            "",
            `${exercise.name} · ${exercise.sets_completed} sets${reps}`
          ));
        });
        card.append(list);
        button.textContent = "Hide exercises −";
        button.setAttribute("aria-expanded", "true");
      } catch (error) {
        historyMessage.textContent = error.message;
      } finally {
        button.disabled = false;
      }
    });
    card.append(button);
    return card;
  }));
}

async function loadHistory() {
  try {
    renderHistory(await requestJson("/api/history"));
  } catch (error) {
    historyList.replaceChildren();
    historyMessage.textContent = error.message;
  }
}

async function loadOptions() {
  try {
    const options = await requestJson("/api/options");
    goalOptions.replaceChildren(...options.goals.map(renderGoalCard));
    goalTrigger.disabled = options.goals.length === 0;
    equipmentOptions.replaceChildren(...options.equipment.map(renderEquipmentOption));
  } catch (error) {
    plannerMessage.textContent = error.message;
  }
}

goalTrigger.addEventListener("click", () => {
  setGoalPickerOpen(goalPopover.hidden);
});

document.addEventListener("click", (event) => {
  if (!goalPicker.contains(event.target)) setGoalPickerOpen(false);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !goalPopover.hidden) {
    setGoalPickerOpen(false);
    goalTrigger.focus();
  }
});

function showPage(pageName) {
  const page = document.querySelector(`#page-${pageName}`);
  if (!page) return;

  document.querySelectorAll(".app-page").forEach((section) => {
    section.hidden = section !== page;
  });
  appNav.querySelectorAll("[data-page-target]").forEach((link) => {
    const active = link.dataset.pageTarget === pageName;
    link.classList.toggle("is-active", active);
    if (active) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
  if (pageName === "tracker") loadHistory();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function setAuthMode(mode) {
  authMode = mode;
  const registering = mode === "register";
  signupNameFields.hidden = !registering;
  authFirstName.required = registering;
  authLastName.required = registering;
  document.querySelector("#signup-welcome").hidden = !registering;
  document.querySelector("#auth-title").textContent = registering ? "Sign up" : "Log in";
  authSubmit.innerHTML = registering
    ? 'Sign up <span aria-hidden="true">→</span>'
    : 'Log in <span aria-hidden="true">→</span>';
  authSwitchCopy.textContent = registering
    ? "Already have an account?"
    : "Don't have an account yet?";
  authSwitchLink.href = registering ? "#login" : "#signup";
  authSwitchLink.innerHTML = registering
    ? 'Log in <span aria-hidden="true">→</span>'
    : 'Sign up now <span aria-hidden="true">→</span>';
  authPassword.autocomplete = registering ? "new-password" : "current-password";
  passwordHint.hidden = !registering;
  authMessage.textContent = "";
}

async function showApp(user) {
  authSection.hidden = true;
  appContent.hidden = false;
  appNav.hidden = false;
  logoutButton.hidden = false;
  welcomeName.textContent = user.first_name ? `${user.first_name}.` : "yourself.";
  document.querySelector("#footer-user").firstElementChild.textContent = `Signed in as ${user.username}`;
  showPage("build");
  await Promise.all([loadOptions(), loadHistory()]);
}

async function checkSession() {
  try {
    const data = await requestJson("/api/auth/me");
    if (data.user) await showApp(data.user);
  } catch (error) {
    authMessage.textContent = error.message;
  }
}

authSwitchLink.addEventListener("click", (event) => {
  event.preventDefault();
  setAuthMode(authMode === "login" ? "register" : "login");
});

appNav.addEventListener("click", (event) => {
  const link = event.target.closest("[data-page-target]");
  if (link) showPage(link.dataset.pageTarget);
});

authForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  authSubmit.disabled = true;
  authMessage.textContent = "";
  try {
    const data = await requestJson(`/api/auth/${authMode}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: document.querySelector("#auth-username").value,
        password: authPassword.value,
        first_name: authFirstName.value,
        last_name: authLastName.value,
      }),
    });
    authForm.reset();
    await showApp(data.user);
  } catch (error) {
    authMessage.textContent = error.message;
  } finally {
    authSubmit.disabled = false;
  }
});

logoutButton.addEventListener("click", async () => {
  logoutButton.disabled = true;
  try {
    await requestJson("/api/auth/logout", { method: "POST" });
    appContent.hidden = true;
    appNav.hidden = true;
    authSection.hidden = false;
    logoutButton.hidden = true;
    historyList.replaceChildren(makeElement("p", "field-hint", "Log in to see your saved workouts."));
    setAuthMode("login");
  } catch (error) {
    historyMessage.textContent = error.message;
  } finally {
    logoutButton.disabled = false;
  }
});

document.querySelector("#planner-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  plannerMessage.textContent = "";
  if (!goalSelect.value) {
    plannerMessage.textContent = "Choose a fitness goal to build your workout.";
    goalTrigger.focus();
    return;
  }
  recommendButton.disabled = true;
  try {
    const duration = Number(durationSelect.value);
    const level = document.querySelector('input[name="level"]:checked').value;
    const data = await requestJson("/api/recommendations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        goal: goalSelect.value,
        level,
        equipment: [...equipmentOptions.querySelectorAll("input:checked")].map((input) => input.value),
        duration,
      }),
    });
    renderRecommendations(data.exercises, goalSelect.value, duration);
  } catch (error) {
    plannerMessage.textContent = error.message;
  } finally {
    recommendButton.disabled = !goalSelect.value;
  }
});

saveButton.addEventListener("click", async () => {
  const completedExercises = [...exerciseList.querySelectorAll(".complete-toggle input:checked")]
    .map((checkbox) => Number(checkbox.value));
  saveButton.disabled = true;
  saveMessage.textContent = "";
  try {
    await requestJson("/api/workouts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        goal: currentGoal,
        completed_exercises: completedExercises,
        notes: document.querySelector("#workout-notes").value,
      }),
    });
    workoutSaved = true;
    saveMessage.textContent = "Workout saved. Nice work showing up!";
    saveMessage.className = "status-message success";
    updateCompletion();
    await loadHistory();
  } catch (error) {
    saveMessage.textContent = error.message;
    updateCompletion();
  }
});

checkSession();
