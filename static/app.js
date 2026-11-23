const goalSelect = document.querySelector("#goal");
const goalPicker = document.querySelector(".goal-picker");
const goalTrigger = document.querySelector("#goal-trigger");
const goalPopover = document.querySelector("#goal-popover");
const goalOptions = document.querySelector("#goal-options");
const goalSelected = document.querySelector("#goal-selected");
const plannerForm = document.querySelector("#planner-form");
const durationSelect = document.querySelector("#duration");
const equipmentOptions = document.querySelector("#equipment-options");
const recommendButton = document.querySelector("#recommend-button");
const plannerMessage = document.querySelector("#planner-message");
const newWorkoutConfirmDialog = document.querySelector("#new-workout-confirm-dialog");
const newWorkoutConfirmTitle = document.querySelector("#new-workout-confirm-title");
const newWorkoutConfirmDescription = document.querySelector("#new-workout-confirm-description");
const newWorkoutConfirmMessage = document.querySelector("#new-workout-confirm-message");
const confirmNewWorkoutButton = document.querySelector("#confirm-new-workout-button");
const cancelNewWorkoutButton = document.querySelector("#cancel-new-workout-button");
const workoutSection = document.querySelector("#workout-section");
const exerciseList = document.querySelector("#exercise-list");
const workoutActions = document.querySelector("#workout-actions");
const startButton = document.querySelector("#start-button");
const saveAndClearButton = document.querySelector("#save-and-clear-button");
const continueWorkoutButton = document.querySelector("#continue-workout-button");
const workoutSheet = document.querySelector("#workout-sheet");
const workoutSheetPanel = document.querySelector("#workout-sheet-panel");
const closeWorkoutSheetButton = document.querySelector("#close-workout-sheet");
const activeStepAnimation = document.querySelector("#active-step-animation");
const workoutProgress = document.querySelector("#workout-progress");
const activeStepPosition = document.querySelector("#active-step-position");
const activeSetCounter = document.querySelector("#active-set-counter");
const activeExerciseTitle = document.querySelector("#active-exercise-title");
const activeExerciseKeywords = document.querySelector("#active-exercise-keywords");
const activeStepPrescription = document.querySelector("#active-step-prescription");
const workoutStepCarousel = document.querySelector("#workout-step-carousel");
const completeStepButton = document.querySelector("#complete-step-button");
const finishWorkoutButton = document.querySelector("#finish-workout-button");
const workoutCompletionOverlay = document.querySelector("#workout-completion-overlay");
const workoutCompletionMessage = document.querySelector("#workout-completion-message");
const activeStepMessage = document.querySelector("#active-step-message");
const activeWorkoutMessage = document.querySelector("#active-workout-message");
const historyList = document.querySelector("#history-list");
const historyMessage = document.querySelector("#history-message");
const pausedWorkoutSection = document.querySelector("#paused-workouts-section");
const pausedWorkoutList = document.querySelector("#paused-workout-list");
const pausedWorkoutMessage = document.querySelector("#paused-workout-message");
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
const workoutThumbnailFrames = new Map();
const welcomeName = document.querySelector("#welcome-name");
const appNav = document.querySelector("#app-nav");
const librarySearchInput = document.querySelector("#library-search");
const libraryEquipmentFilters = document.querySelector("#library-equipment-filters");
const libraryTargetFilters = document.querySelector("#library-target-filters");
const libraryStatus = document.querySelector("#library-status");
const libraryResultCount = document.querySelector("#library-result-count");
const libraryExerciseGrid = document.querySelector("#library-exercise-grid");
const libraryEmpty = document.querySelector("#library-empty");
const exerciseHoverPreview = document.querySelector("#exercise-hover-preview");
const exerciseHoverPreviewContent = document.querySelector("#exercise-hover-preview-content");
const exercisePreviewDialog = document.querySelector("#exercise-preview-dialog");
const exercisePreviewDialogContent = document.querySelector("#exercise-preview-dialog-content");
const exercisePreviewCloseButton = document.querySelector("#exercise-preview-close");
let currentGoal = "";
let currentLevel = "";
let currentEquipment = [];
let currentExercises = [];
let currentDuration = 0;
let currentRecommendationSeed = null;
let workoutSteps = [];
let currentWorkoutStepIndex = 0;
let completedWorkoutSteps = new Set();
let currentWorkoutSessionId = null;
let currentWorkoutStructureMode = "block";
let currentWorkoutNotes = "";
let pendingNewWorkoutAction = null;
let pendingWorkoutToPause = null;
let skipWorkoutConflictCheck = false;
let workoutCloseInProgress = false;
let workoutProgressSaving = false;
let libraryExercises = [];
let libraryLoaded = false;
let libraryLoading = false;
const selectedLibraryEquipment = new Set();
const selectedLibraryTargets = new Set();
let authMode = "login";

function openWorkoutSheet() {
  workoutSheet.hidden = false;
  workoutSheetPanel.setAttribute("aria-hidden", "false");
  document.body.classList.add("workout-sheet-open");
  requestAnimationFrame(() => {
    if (!workoutSheet.hidden) workoutSheet.classList.add("is-open");
  });
  closeWorkoutSheetButton.focus();
}

function finishWorkoutSheetClose() {
  workoutSheet.hidden = true;
  document.body.classList.remove("workout-sheet-open");
  document.querySelector(
    workoutSection.hidden ? "#planner-title" : "#workout-title"
  ).focus();
}

async function closeWorkoutSheet() {
  if (workoutCloseInProgress) return;
  if (currentWorkoutSessionId) {
    if (workoutProgressSaving) {
      activeStepMessage.textContent = "Please wait for this set to save before exiting.";
      return;
    }
    workoutCloseInProgress = true;
    closeWorkoutSheetButton.disabled = true;
    try {
      await pauseWorkout({
        session_id: currentWorkoutSessionId,
        structure_mode: currentWorkoutStructureMode,
        completed_set_keys: [...completedWorkoutSteps],
        notes: currentWorkoutNotes,
      });
      hideGeneratedWorkout();
      await loadPausedWorkouts();
    } catch (error) {
      activeStepMessage.textContent = `Could not save workout progress: ${error.message}`;
      return;
    } finally {
      workoutCloseInProgress = false;
      closeWorkoutSheetButton.disabled = false;
    }
  }
  if (!workoutSheet.classList.contains("is-open")) {
    finishWorkoutSheetClose();
    return;
  }
  workoutSheet.classList.remove("is-open");
  workoutSheetPanel.setAttribute("aria-hidden", "true");
}

workoutSheetPanel.addEventListener("transitionend", (event) => {
  if (event.propertyName === "transform" && !workoutSheet.classList.contains("is-open")) {
    finishWorkoutSheetClose();
  }
});

closeWorkoutSheetButton.addEventListener("click", closeWorkoutSheet);
workoutSheet.querySelector(".workout-sheet-backdrop").addEventListener("click", closeWorkoutSheet);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !workoutSheet.hidden) closeWorkoutSheet();
});

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

const goalImages = {
  accessibility: "accessibility.jpg",
  balance: "balance.jpg",
  cardio: "cardio.jpg",
  cool_down: "cooldown.jpg",
  coordination: "coordination.jpg",
  core_stability: "core-stability.jpg",
  first_pushup: "first-push-up.jpg",
  hip_stability: "hip-stability.jpg",
  lower_body_strength: "lower-body.jpg",
  mobility: "mobility.jpg",
  overall_fitness: "overall-fitness.jpg",
  posture: "posture.jpg",
  upper_body_strength: "upper-body.jpg",
  warm_up: "warm-up.jpg",
};

function renderGoalCard(goal) {
  const card = makeElement("button", "goal-card");
  card.type = "button";
  card.dataset.goal = goal;
  card.setAttribute("aria-pressed", "false");

  const imageFile = goalImages[goal];
  const image = makeElement(imageFile ? "img" : "span", imageFile ? "goal-image" : "goal-image-placeholder");
  if (imageFile) {
    image.src = `/static/workout-focus/${imageFile}`;
    image.alt = "";
    image.loading = "lazy";
    image.decoding = "async";
  } else {
    image.setAttribute("role", "img");
    image.setAttribute("aria-label", `${prettyLabel(goal)} image placeholder`);
    image.innerHTML = '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="15"/><circle cx="24" cy="24" r="8"/><circle cx="24" cy="24" r="2"/><path d="m32 16 8-8m-5 0h5v5"/></svg><span>Image soon</span>';
  }
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
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    const message = response.status === 404
      ? "The server does not recognize this API route. Restart Flask to load the latest changes."
      : `The server returned an unexpected response (${response.status}). Please try again.`;
    throw new Error(message);
  }
  const data = await response.json();
  if (!response.ok) {
    const error = new Error(data.error || "Something went wrong. Please try again.");
    error.status = response.status;
    throw error;
  }
  return data;
}

function isValidStoredExercise(exercise) {
  const optionalNumber = (value) => value === null || Number.isFinite(value);
  return exercise !== null
    && typeof exercise === "object"
    && Number.isInteger(exercise.id)
    && typeof exercise.name === "string"
    && Number.isInteger(exercise.sets)
    && exercise.sets >= 1
    && exercise.sets <= 20
    && Number.isFinite(exercise.duration)
    && optionalNumber(exercise.reps)
    && optionalNumber(exercise.hold_seconds)
    && optionalNumber(exercise.work_seconds)
    && optionalNumber(exercise.rest_seconds)
    && typeof exercise.level === "string"
    && (exercise.goals === undefined
      || (Array.isArray(exercise.goals)
        && exercise.goals.every((goal) => typeof goal === "string")))
    && (exercise.keywords === undefined
      || (Array.isArray(exercise.keywords)
        && exercise.keywords.every((keyword) => typeof keyword === "string")))
    && Array.isArray(exercise.instructions)
    && exercise.instructions.every((instruction) => typeof instruction === "string")
    && Array.isArray(exercise.equipment)
    && exercise.equipment.every((item) => typeof item === "string")
    && (exercise.media_url === null
      || (typeof exercise.media_url === "string" && exercise.media_url.startsWith("/static/")))
    && (exercise.media_type === null
      || ["gif", "mp4", "jpg", "jpeg", "png", "webp"].includes(exercise.media_type));
}

function isValidStoredWorkout(workout, availableGoals) {
  return workout !== null
    && typeof workout === "object"
    && workout.version === 1
    && typeof workout.session_id === "string"
    && workout.session_id.length > 0
    && availableGoals.includes(workout.goal)
    && ["beginner", "intermediate", "advanced"].includes(workout.level)
    && Number.isInteger(workout.duration)
    && workout.duration >= 15
    && workout.duration <= 180
    && workout.duration % 15 === 0
    && Array.isArray(workout.equipment)
    && workout.equipment.every((item) => typeof item === "string")
    && Array.isArray(workout.exercises)
    && workout.exercises.length > 0
    && workout.exercises.length <= 30
    && workout.exercises.every(isValidStoredExercise)
    && Array.isArray(workout.completed_set_keys)
    && workout.completed_set_keys.length <= 600
    && workout.completed_set_keys.every((key) => typeof key === "string")
    && typeof workout.saved === "boolean"
    && typeof workout.notes === "string";
}

function buildWorkoutSteps(exercises) {
  return exercises.flatMap((exercise, exerciseIndex) =>
    Array.from({ length: exercise.sets }, (_, setIndex) => ({
      exercise,
      exerciseIndex,
      setNumber: setIndex + 1,
      key: `${exercise.id}:${setIndex + 1}`,
    }))
  );
}

function createExerciseMedia(
  exercise,
  mediaClass = "exercise-media",
  placeholderClass = "media-placeholder",
  autoplay = false,
  controls = true
) {
  if (exercise.media_url && exercise.media_type === "mp4") {
    const video = makeElement("video", mediaClass);
    video.controls = controls;
    video.muted = true;
    video.loop = true;
    video.playsInline = true;
    video.autoplay = autoplay;
    video.preload = autoplay ? "auto" : "metadata";
    video.addEventListener("loadedmetadata", () => {
      video.classList.toggle("is-portrait", video.videoHeight > video.videoWidth);
    });
    const source = makeElement("source");
    source.src = exercise.media_url;
    source.type = "video/mp4";
    video.append(source);
    return video;
  }
  if (exercise.media_url) {
    const image = makeElement("img", mediaClass);
    image.src = exercise.media_url;
    const isStaticIllustration = ["jpg", "jpeg", "png", "webp"]
      .includes(exercise.media_type);
    image.alt = isStaticIllustration
      ? `${exercise.name} key-position illustration`
      : `${exercise.name} demonstration`;
    return image;
  }
  return makeElement("div", placeholderClass, "Demo coming soon");
}

function populateExercisePreview(container, exercise, titleId) {
  const preview = makeElement("article", "exercise-preview");
  const mediaFrame = makeElement("div", "exercise-preview-visual");
  mediaFrame.append(createExerciseMedia(
    exercise,
    "exercise-preview-media",
    "exercise-preview-placeholder",
    true,
    true
  ));
  preview.append(mediaFrame);

  const details = makeElement("div", "exercise-preview-details");
  const heading = makeElement("div", "exercise-preview-heading");
  const title = makeElement("h2", "exercise-preview-title", exercise.name);
  title.id = titleId;
  heading.append(title);
  details.append(heading);

  const stats = makeElement("dl", "exercise-preview-stats");
  const facts = makeElement("dl", "exercise-preview-facts");
  const addInformation = (container, label, value, className) => {
    if (value === null || value === undefined || value === "") return;
    const item = makeElement("div", className);
    item.append(
      makeElement("dt", "", label),
      makeElement("dd", "", value)
    );
    container.append(item);
  };
  const addStat = (label, value) => {
    addInformation(stats, label, value, "exercise-preview-stat");
  };
  const addFact = (label, value) => {
    addInformation(facts, label, value, "exercise-preview-fact");
  };

  if (typeof exercise.level === "string" && exercise.level) {
    addStat("Difficulty", prettyLabel(exercise.level));
  }
  if (Number.isFinite(exercise.duration)) {
    addStat("Duration", `${exercise.duration} min`);
  }
  if (Number.isFinite(exercise.sets)) {
    addStat("Sets", String(exercise.sets));
  }
  if (Number.isFinite(exercise.reps)) {
    addStat("Reps", String(exercise.reps));
  } else if (Number.isFinite(exercise.hold_seconds)) {
    addStat("Hold", `${exercise.hold_seconds} sec`);
  } else if (Number.isFinite(exercise.work_seconds)) {
    addStat("Work", `${exercise.work_seconds} sec`);
  }
  if (stats.children.length) details.append(stats);

  if (Array.isArray(exercise.body_area) && exercise.body_area.length) {
    addFact("Target muscles", exercise.body_area.map(prettyLabel).join(", "));
  }
  if (Array.isArray(exercise.equipment)) {
    addFact(
      "Equipment",
      exercise.equipment.length
        ? exercise.equipment.map(prettyLabel).join(", ")
        : "None required"
    );
  }
  if (Number.isFinite(exercise.rest_seconds) && exercise.rest_seconds > 0) {
    addFact("Rest between sets", `${exercise.rest_seconds} sec`);
  }
  if (facts.children.length) details.append(facts);

  if (Array.isArray(exercise.instructions) && exercise.instructions.length) {
    const instructions = makeElement("section", "exercise-preview-instructions");
    instructions.append(makeElement("h3", "", "How to Perform"));
    const steps = makeElement("ol");
    exercise.instructions.forEach((instruction) => {
      steps.append(makeElement("li", "", instruction));
    });
    instructions.append(steps);
    details.append(instructions);
  }

  preview.append(details);
  container.replaceChildren(preview);
}

const exercisePreviewHoverQuery = window.matchMedia("(hover: hover) and (pointer: fine)");
let activeExercisePreviewTrigger = null;
let exercisePreviewReturnFocus = null;

function closeExerciseHoverPreview() {
  exerciseHoverPreview.classList.remove("is-visible");
  exerciseHoverPreview.setAttribute("aria-hidden", "true");
  exerciseHoverPreview.hidden = true;
  exerciseHoverPreviewContent.replaceChildren();
  activeExercisePreviewTrigger = null;
}

function positionExerciseHoverPreview() {
  if (exerciseHoverPreview.hidden || !activeExercisePreviewTrigger) return;

  const anchor = activeExercisePreviewTrigger.getBoundingClientRect();
  const panel = exerciseHoverPreview.getBoundingClientRect();
  const padding = 12;
  const gap = 14;
  const maxLeft = Math.max(padding, window.innerWidth - panel.width - padding);
  const maxTop = Math.max(padding, window.innerHeight - panel.height - padding);
  let left = anchor.right + gap;

  if (left + panel.width > window.innerWidth - padding) {
    left = anchor.left - panel.width - gap;
  }
  if (left < padding || left > maxLeft) {
    left = Math.min(
      maxLeft,
      Math.max(padding, anchor.left + (anchor.width - panel.width) / 2)
    );
  }

  let top = anchor.top;
  if (top + panel.height > window.innerHeight - padding) {
    top = anchor.bottom - panel.height;
  }
  top = Math.min(maxTop, Math.max(padding, top));
  exerciseHoverPreview.style.left = `${left}px`;
  exerciseHoverPreview.style.top = `${top}px`;
}

function showExerciseHoverPreview(trigger, exercise) {
  if (exercisePreviewDialog.open) return;
  activeExercisePreviewTrigger = trigger;
  exerciseHoverPreview.hidden = false;
  exerciseHoverPreview.setAttribute("aria-hidden", "false");
  exerciseHoverPreview.setAttribute(
    "aria-label",
    `${exercise.name} exercise preview`
  );
  populateExercisePreview(
    exerciseHoverPreviewContent,
    exercise,
    "exercise-hover-preview-title"
  );
  positionExerciseHoverPreview();
  exerciseHoverPreview.getBoundingClientRect();
  exerciseHoverPreview.classList.add("is-visible");
}

function updateExerciseHoverPreviewPosition() {
  if (exerciseHoverPreview.hidden || !activeExercisePreviewTrigger) return;
  if (!activeExercisePreviewTrigger.matches(":hover")) {
    closeExerciseHoverPreview();
    return;
  }
  positionExerciseHoverPreview();
}

function openExercisePreviewDialog(trigger, exercise) {
  closeExerciseHoverPreview();
  exercisePreviewReturnFocus = trigger;
  populateExercisePreview(
    exercisePreviewDialogContent,
    exercise,
    "exercise-preview-dialog-title"
  );
  exercisePreviewDialog.showModal();
}

function attachExercisePreview(card, exercise) {
  card.tabIndex = 0;
  card.setAttribute("role", "button");
  card.setAttribute("aria-haspopup", "dialog");
  card.setAttribute("aria-controls", "exercise-preview-dialog");
  card.setAttribute("aria-label", `Open exercise preview for ${exercise.name}`);

  card.addEventListener("pointerenter", (event) => {
    if (exercisePreviewHoverQuery.matches && event.pointerType !== "touch") {
      showExerciseHoverPreview(card, exercise);
    }
  });
  card.addEventListener("pointerleave", () => {
    if (exercisePreviewHoverQuery.matches) closeExerciseHoverPreview();
  });
  card.addEventListener("click", () => {
    if (!exercisePreviewDialog.open) openExercisePreviewDialog(card, exercise);
  });
  card.addEventListener("keydown", (event) => {
    if (event.target !== card || !["Enter", " "].includes(event.key)) return;
    event.preventDefault();
    if (!exercisePreviewDialog.open) openExercisePreviewDialog(card, exercise);
  });
}

exercisePreviewCloseButton.addEventListener("click", () => {
  exercisePreviewDialog.close();
});
exercisePreviewDialog.addEventListener("click", (event) => {
  if (event.target === exercisePreviewDialog) exercisePreviewDialog.close();
});
exercisePreviewDialog.addEventListener("close", () => {
  exercisePreviewDialogContent.replaceChildren();
  if (exercisePreviewReturnFocus?.isConnected) exercisePreviewReturnFocus.focus();
  exercisePreviewReturnFocus = null;
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && exercisePreviewDialog.open) {
    event.preventDefault();
    exercisePreviewDialog.close();
    return;
  }
  if (
    event.key === "Escape"
    && !exercisePreviewDialog.open
    && !exerciseHoverPreview.hidden
  ) {
    closeExerciseHoverPreview();
  }
});
window.addEventListener("resize", updateExerciseHoverPreviewPosition);
window.addEventListener("scroll", updateExerciseHoverPreviewPosition, true);

function renderCurrentWorkoutStep(message = "") {
  const step = workoutSteps[currentWorkoutStepIndex];
  if (!step) return;

  const { exercise, exerciseIndex, setNumber } = step;
  activeStepPosition.textContent = `Exercise ${exerciseIndex + 1} of ${currentExercises.length}`;
  activeSetCounter.textContent = `Set ${setNumber} of ${exercise.sets}`;
  activeExerciseTitle.textContent = `of ${exercise.name}`;
  activeExerciseKeywords.textContent = (exercise.keywords || [])
    .map(prettyLabel)
    .join(" · ");

  activeStepPrescription.replaceChildren();
  let prescription = "";
  if (exercise.reps !== null) prescription = `${exercise.reps} reps`;
  else if (exercise.hold_seconds !== null) prescription = `${exercise.hold_seconds}s hold`;
  else if (exercise.work_seconds !== null) prescription = `${exercise.work_seconds}s work`;
  if (prescription) {
    activeStepPrescription.append(makeElement("li", "active-step-main-prescription", prescription));
  }
  if (Number.isFinite(exercise.rest_seconds) && exercise.rest_seconds > 0) {
    activeStepPrescription.append(makeElement(
      "li",
      "active-step-rest",
      `${exercise.rest_seconds}s rest between sets`
    ));
  }

  activeStepAnimation.replaceChildren(
    createExerciseMedia(exercise, "active-exercise-media", "active-step-placeholder", true)
  );
  const isComplete = completedWorkoutSteps.has(step.key);
  const workoutComplete = workoutSteps.length > 0
    && completedWorkoutSteps.size === workoutSteps.length;
  const shouldFocusFinishButton = workoutComplete && workoutCompletionOverlay.hidden;
  completeStepButton.textContent = isComplete ? "Mark set incomplete" : "Done, next set";
  finishWorkoutButton.hidden = !workoutComplete;
  workoutCompletionOverlay.hidden = !workoutComplete;
  workoutSheetPanel.classList.toggle("workout-complete", workoutComplete);
  workoutCompletionMessage.textContent = workoutComplete ? message : "";
  activeStepMessage.textContent = workoutComplete ? "" : message;
  renderWorkoutProgress();
  if (shouldFocusFinishButton) finishWorkoutButton.focus();
}

function renderWorkoutProgress() {
  workoutProgress.replaceChildren(...workoutSteps.map((step, index) => {
    const segment = makeElement("span", "workout-progress-segment");
    segment.setAttribute("aria-hidden", "true");
    segment.classList.toggle("is-complete", completedWorkoutSteps.has(step.key));
    segment.classList.toggle("is-current", index === currentWorkoutStepIndex);
    return segment;
  }));
  workoutProgress.setAttribute("aria-valuemax", String(workoutSteps.length));
  workoutProgress.setAttribute("aria-valuenow", String(completedWorkoutSteps.size));
  renderWorkoutStepCarousel();
}

function createExerciseThumbnail(exercise, mediaClass, placeholderClass) {
  if (!exercise.media_url) {
    return makeElement("div", placeholderClass, "Demo coming soon");
  }
  if (exercise.media_type !== "gif" && exercise.media_type !== "mp4") {
    return createExerciseMedia(
      exercise,
      mediaClass,
      placeholderClass,
      false,
      false
    );
  }

  const thumbnail = makeElement("img", mediaClass);
  thumbnail.alt = `${exercise.name} demonstration preview`;
  let framePromise = workoutThumbnailFrames.get(exercise.media_url);
  if (!framePromise) {
    framePromise = new Promise((resolve, reject) => {
      const isVideo = exercise.media_type === "mp4";
      const source = isVideo ? document.createElement("video") : new Image();
      source.addEventListener(isVideo ? "loadeddata" : "load", () => {
        const width = isVideo ? source.videoWidth : source.naturalWidth;
        const height = isVideo ? source.videoHeight : source.naturalHeight;
        if (!width || !height) {
          reject(new Error(`Could not read thumbnail dimensions for ${exercise.name}.`));
          return;
        }

        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        const context = canvas.getContext("2d");
        if (!context) {
          reject(new Error("Could not create a canvas to capture the exercise thumbnail."));
          return;
        }

        try {
          context.drawImage(source, 0, 0, width, height);
          resolve({ src: canvas.toDataURL("image/png"), isPortrait: height > width });
        } catch (error) {
          reject(error);
        } finally {
          if (isVideo) {
            source.pause();
            source.removeAttribute("src");
            source.load();
          }
        }
      }, { once: true });
      source.addEventListener("error", () => {
        reject(new Error(`Could not load thumbnail media for ${exercise.name}.`));
      }, { once: true });
      if (isVideo) {
        source.muted = true;
        source.preload = "auto";
        source.playsInline = true;
      }
      source.src = exercise.media_url;
      if (isVideo) source.load();
    });
    workoutThumbnailFrames.set(exercise.media_url, framePromise);
  }

  framePromise.then(({ src, isPortrait }) => {
    thumbnail.src = src;
    thumbnail.classList.toggle("is-portrait", isPortrait);
  }).catch((error) => {
    console.error(`Unable to create a static thumbnail for ${exercise.name}.`, error);
  });
  return thumbnail;
}

function renderWorkoutStepCarousel() {
  workoutStepCarousel.replaceChildren(...workoutSteps.map((step, index) => {
    const completed = completedWorkoutSteps.has(step.key);
    const thumbnail = makeElement("button", "workout-step-thumbnail");
    thumbnail.type = "button";
    thumbnail.classList.toggle("is-current", index === currentWorkoutStepIndex);
    thumbnail.classList.toggle("is-complete", completed);
    thumbnail.setAttribute("aria-current", index === currentWorkoutStepIndex ? "step" : "false");
    thumbnail.setAttribute(
      "aria-label",
      `${step.exercise.name}, set ${step.setNumber}${completed ? ", completed" : ""}`
    );

    thumbnail.append(createExerciseThumbnail(
      step.exercise,
      "workout-step-thumbnail-media",
      "workout-step-thumbnail-placeholder"
    ));
    const details = makeElement("span", "workout-step-thumbnail-details");
    details.append(
      makeElement("span", "workout-step-thumbnail-name", step.exercise.name),
      makeElement("span", "workout-step-thumbnail-set", `Set ${step.setNumber}`)
    );
    thumbnail.append(details);
    thumbnail.append(makeElement("span", "workout-step-thumbnail-check", completed ? "✓" : ""));
    thumbnail.addEventListener("click", () => {
      currentWorkoutStepIndex = index;
      renderCurrentWorkoutStep();
    });
    return thumbnail;
  }));
  const currentThumbnail = workoutStepCarousel.querySelector(".is-current");
  if (currentThumbnail) {
    currentThumbnail.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
  }
}

function renderActiveWorkout(workout) {
  const availableGoals = [...goalOptions.querySelectorAll(".goal-card")]
    .map((card) => card.dataset.goal);
  if (!isValidStoredWorkout(workout, availableGoals)) {
    plannerMessage.textContent = "Your saved workout could not be restored. Please start a new workout.";
    return;
  }

  currentGoal = workout.goal;
  currentLevel = workout.level;
  currentEquipment = workout.equipment;
  currentWorkoutSessionId = workout.session_id;
  currentWorkoutStructureMode = workout.structure_mode;
  currentWorkoutNotes = workout.notes || "";
  currentExercises = workout.exercises;
  currentDuration = workout.duration;
  workoutSteps = buildWorkoutSteps(currentExercises);
  const validStepKeys = new Set(workoutSteps.map((step) => step.key));
  completedWorkoutSteps = new Set(
    workout.completed_set_keys.filter((key) => validStepKeys.has(key))
  );
  currentWorkoutStepIndex = workoutSteps.findIndex(
    (step) => !completedWorkoutSteps.has(step.key)
  );
  if (currentWorkoutStepIndex === -1) currentWorkoutStepIndex = 0;
  selectGoal(workout.goal);
  durationSelect.value = String(workout.duration);
  document.querySelectorAll('input[name="level"]').forEach((input) => {
    input.checked = input.value === workout.level;
  });
  equipmentOptions.querySelectorAll('input[name="equipment"]').forEach((input) => {
    input.checked = workout.equipment.includes(input.value);
  });
  document.querySelector("#workout-focus").textContent = prettyLabel(workout.goal);
  document.querySelector("#workout-level").textContent = prettyLabel(workout.level);
  document.querySelector("#workout-duration").textContent = `${workout.duration} minutes`;
  workoutActions.hidden = false;
  startButton.hidden = true;
  saveAndClearButton.hidden = false;
  continueWorkoutButton.hidden = false;
  document.querySelector("#no-results").hidden = true;
  workoutSection.classList.add("is-in-progress");
  workoutSection.hidden = false;
  activeWorkoutMessage.textContent = "";
  activeWorkoutMessage.className = "status-message";
  renderExercises();
  renderCurrentWorkoutStep();
  workoutSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function hideGeneratedWorkout() {
  workoutSection.hidden = true;
  workoutSection.classList.remove("is-in-progress");
  workoutActions.hidden = true;
  startButton.hidden = true;
  saveAndClearButton.hidden = true;
  continueWorkoutButton.hidden = true;
  exerciseList.replaceChildren();
  currentWorkoutSessionId = null;
  currentExercises = [];
  currentDuration = 0;
  currentRecommendationSeed = null;
  workoutSteps = [];
  currentWorkoutStepIndex = 0;
  completedWorkoutSteps.clear();
  finishWorkoutButton.hidden = true;
  workoutCompletionOverlay.hidden = true;
  workoutSheetPanel.classList.remove("workout-complete");
  activeWorkoutMessage.textContent = "";
}

async function pauseWorkout(workout) {
  if (!workout || typeof workout.session_id !== "string" || !workout.session_id) {
    throw new Error("There is no active workout to save.");
  }
  await requestJson("/api/active-workout/pause", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: workout.session_id,
      structure_mode: workout.structure_mode || "block",
      completed_set_keys: Array.isArray(workout.completed_set_keys)
        ? workout.completed_set_keys
        : [],
      notes: workout.notes || "",
    }),
  });
}

function promptToReplaceWorkout(action, workout, sessionId = null) {
  pendingNewWorkoutAction = { action, sessionId };
  pendingWorkoutToPause = workout;
  const hasActiveWorkout = Boolean(workout);
  const actionLabels = {
    create: ["Start a new workout?", "create new"],
    start: ["Start a new workout?", "create new"],
    redo: ["Redo this workout?", "redo workout"],
    resume: ["Resume another workout?", "resume workout"],
  };
  const [title, buttonLabel] = actionLabels[action];
  newWorkoutConfirmTitle.textContent = title;
  newWorkoutConfirmDescription.textContent = hasActiveWorkout
    ? "Your current workout and completed sets will be saved in History so you can resume it later."
    : "Your unfinished workouts are already saved in History and will remain available.";
  confirmNewWorkoutButton.textContent = hasActiveWorkout
    ? `Yes, save and ${buttonLabel}`
    : `Yes, ${buttonLabel}`;
  newWorkoutConfirmMessage.textContent = "";
  newWorkoutConfirmDialog.showModal();
}

function renderExercise(exercise) {
  const card = makeElement("article", "exercise-card");
  card.dataset.exerciseId = String(exercise.id);
  card.append(createExerciseMedia(exercise));

  const content = makeElement("div", "exercise-content");
  const heading = makeElement("div", "exercise-top");
  heading.append(makeElement("h3", "exercise-title", exercise.name));
  content.append(heading);

  const keywords = (exercise.keywords || []).map(prettyLabel);
  if (keywords.length) {
    content.append(makeElement("p", "exercise-keywords", keywords.join(" · ")));
  }

  const equipment = makeElement("div", "exercise-equipment");
  equipment.setAttribute("aria-label", "Required equipment");
  if (exercise.equipment.length) {
    exercise.equipment.forEach((item) => {
      const equipmentItem = makeElement("span", "exercise-equipment-item");
      const icon = makeElement("span", "equipment-icon");
      icon.setAttribute("aria-hidden", "true");
      icon.innerHTML = equipmentIcons[item] || equipmentIcons.bar;
      equipmentItem.append(icon, makeElement("span", "exercise-equipment-name", prettyLabel(item)));
      equipment.append(equipmentItem);
    });
  } else {
    equipment.append(makeElement("span", "no-required-equipment", "No required equipment"));
  }
  content.append(equipment);

  const specifics = makeElement("ul", "exercise-specifics");
  const setCount = `${exercise.sets} ${exercise.sets === 1 ? "set" : "sets"}`;
  let prescription = "";
  if (exercise.reps !== null) prescription = ` × ${exercise.reps} reps`;
  else if (exercise.hold_seconds !== null) prescription = ` × ${exercise.hold_seconds}s hold`;
  else if (exercise.work_seconds !== null) prescription = ` × ${exercise.work_seconds}s work`;
  specifics.append(makeElement("li", "", `${setCount}${prescription}`));
  if (Number.isFinite(exercise.rest_seconds) && exercise.rest_seconds > 0) {
    specifics.append(makeElement("li", "", `${exercise.rest_seconds}s rest between sets`));
  }
  content.append(specifics);
  card.append(content);
  attachExercisePreview(card, exercise);
  return card;
}

function renderExercises() {
  closeExerciseHoverPreview();
  exerciseList.replaceChildren(...currentExercises.map(renderExercise));
}


completeStepButton.addEventListener("click", async () => {
  if (workoutCloseInProgress) return;
  const step = workoutSteps[currentWorkoutStepIndex];
  if (!step) return;

  if (!currentWorkoutSessionId) {
    activeStepMessage.textContent = "Please start your workout first.";
    return;
  }

  // Keep a copy in case saving fails.
  const previousCompletedSets = new Set(completedWorkoutSteps);
  const previousStepIndex = currentWorkoutStepIndex;

  if (completedWorkoutSteps.has(step.key)) {
    completedWorkoutSteps.delete(step.key);
  } else {
    completedWorkoutSteps.add(step.key);

    const hasNextStep = currentWorkoutStepIndex < workoutSteps.length - 1;
    if (hasNextStep) currentWorkoutStepIndex += 1;
  }

  completeStepButton.disabled = true;
  workoutProgressSaving = true;
  activeStepMessage.textContent = "Saving progress...";

  try {
    await requestJson("/api/active-workout", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        session_id: currentWorkoutSessionId,
        structure_mode: currentWorkoutStructureMode,
        completed_set_keys: [...completedWorkoutSteps],
        notes: currentWorkoutNotes
      })
    });

    renderCurrentWorkoutStep();

  } catch (error) {
    // Restore the previous state if saving fails.
    completedWorkoutSteps = previousCompletedSets;
    currentWorkoutStepIndex = previousStepIndex;

    renderCurrentWorkoutStep("Could not save progress: " + error.message);
  } finally {
    workoutProgressSaving = false;
    completeStepButton.disabled = false;
  }
});

finishWorkoutButton.addEventListener("click", async () => {
  if (completedWorkoutSteps.size !== workoutSteps.length) {
    activeStepMessage.textContent = "Complete all sets before finishing.";
    return;
  }

  finishWorkoutButton.disabled = true;
  workoutCompletionMessage.textContent = "Saving workout to your history...";
  finishWorkoutButton.textContent = "Saving...";

  try {
    await requestJson("/api/workouts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        session_id: currentWorkoutSessionId,
        structure_mode: currentWorkoutStructureMode,
        completed_set_keys: [...completedWorkoutSteps],
        notes: currentWorkoutNotes
      })
    });

    currentWorkoutSessionId = null;
    hideGeneratedWorkout();

    closeWorkoutSheet();

await Promise.all([
  loadHistory(),
  loadStats()
]);

  } catch (error) {
    workoutCompletionMessage.textContent = "Could not finish workout: " + error.message;
  } finally {
    finishWorkoutButton.disabled = false;
    finishWorkoutButton.textContent = "Finish workout";
  }
});

function renderEmptyWorkout(goal, level, duration, message) {
  currentGoal = goal;
  currentExercises = [];
  currentDuration = duration;
  workoutSteps = [];
  currentWorkoutStepIndex = 0;
  completedWorkoutSteps.clear();
  document.querySelector("#workout-focus").textContent = prettyLabel(goal);
  document.querySelector("#workout-level").textContent = prettyLabel(level);
  document.querySelector("#workout-duration").textContent = `${duration} minutes`;
  closeExerciseHoverPreview();
  exerciseList.replaceChildren();
  const noResults = document.querySelector("#no-results");
  noResults.hidden = false;
  noResults.textContent = message;
  workoutSection.hidden = false;
  workoutActions.hidden = true;
  startButton.hidden = true;
  continueWorkoutButton.hidden = true;
  saveAndClearButton.hidden = true;
  activeWorkoutMessage.textContent = "";
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
    


    const redoButton = makeElement("button", "history-redo", "Redo workout");
    redoButton.type = "button";

    redoButton.addEventListener("click", async () => {
      redoButton.disabled = true;
      redoButton.textContent = "Preparing workout...";

      try {
        const [active, paused] = await Promise.all([
          requestJson("/api/active-workout"),
          requestJson("/api/paused-workouts"),
        ]);
        if (active.active_workout || paused.paused_workouts.length > 0) {
          promptToReplaceWorkout("redo", active.active_workout, workout.session_id);
        } else {
          await redoSavedWorkout(workout.session_id);
        }

      } catch (error) {
        historyMessage.textContent = error.message;
      } finally {
        redoButton.disabled = false;
        redoButton.textContent = "Redo workout";
      }
    });

    const historyActions = makeElement("div", "history-actions");
    historyActions.append(button, redoButton);
    card.append(historyActions);

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

function renderPausedWorkouts(workouts) {
  pausedWorkoutMessage.textContent = "";
  pausedWorkoutList.replaceChildren();
  pausedWorkoutSection.hidden = workouts.length === 0;
  if (workouts.length === 0) return;

  pausedWorkoutList.replaceChildren(...workouts.map((workout) => {
    const card = makeElement("article", "history-card");
    const main = makeElement("div", "history-main");
    const summary = makeElement("div");
    const totalSets = workout.exercises.reduce(
      (total, exercise) => total + exercise.sets,
      0
    );
    summary.append(makeElement(
      "p",
      "history-date",
      `${prettyLabel(workout.goal)} workout`
    ));
    summary.append(makeElement(
      "p",
      "history-detail",
      `${workout.completed_set_keys.length} of ${totalSets} sets saved · ${workout.duration} min`
    ));
    main.append(summary, makeElement("span", "history-goal", "Unfinished"));
    card.append(main);

    const resumeButton = makeElement("button", "button button-secondary", "Resume workout");
    resumeButton.type = "button";
    resumeButton.addEventListener("click", async () => {
      resumeButton.disabled = true;
      resumeButton.textContent = "Resuming...";
      pausedWorkoutMessage.textContent = "";
      try {
        const active = await requestJson("/api/active-workout");
        if (active.active_workout) {
          promptToReplaceWorkout("resume", active.active_workout, workout.session_id);
        } else {
          await resumeSavedWorkout(workout.session_id);
        }
      } catch (error) {
        pausedWorkoutMessage.textContent = error.message;
      } finally {
        resumeButton.disabled = false;
        resumeButton.textContent = "Resume workout";
      }
    });

    const actions = makeElement("div", "history-actions paused-workout-actions");
    actions.append(resumeButton);
    card.append(actions);
    return card;
  }));
}

async function loadPausedWorkouts() {
  try {
    const data = await requestJson("/api/paused-workouts");
    renderPausedWorkouts(data.paused_workouts);
  } catch (error) {
    pausedWorkoutList.replaceChildren();
    pausedWorkoutSection.hidden = false;
    pausedWorkoutMessage.textContent = error.message;
  }
}

async function resumeSavedWorkout(sessionId) {
  const result = await requestJson(
    `/api/paused-workouts/${encodeURIComponent(sessionId)}/resume`,
    { method: "POST" }
  );
  showPage("build");
  renderActiveWorkout(result.active_workout);
  openWorkoutSheet();
  await loadPausedWorkouts();
}

async function redoSavedWorkout(sessionId) {
  const result = await requestJson(
    `/api/history/${encodeURIComponent(sessionId)}/redo`,
    { method: "POST" }
  );
  showPage("build");
  renderActiveWorkout(result.active_workout);
  openWorkoutSheet();
  await loadPausedWorkouts();
}

async function loadStats(period = "week") {
  try {
    const stats = await requestJson(`/api/stats?period=${period}`);

    document.querySelector("#stats-period-label").textContent =
      period === "week" ? "Your progress this week" : "Your progress this year";
    document.querySelector("#stats-activity-label").textContent =
      period === "week"
        ? "Your completed workouts by day of the week"
        : "Your completed workouts by month";

    document.querySelector("#stat-sessions").textContent =
      stats.total_sessions;

    document.querySelector("#stat-days").textContent =
      stats.workout_days;

    document.querySelector("#stat-minutes").textContent =
      stats.total_duration;

    document.querySelector("#stat-sets").textContent =
      stats.total_sets;

    document.querySelector("#stats-message").textContent = "";
    const chart = document.querySelector("#stats-chart");
    chart.replaceChildren();

    if (!stats.activity || stats.activity.length === 0) {
      chart.textContent = "No workouts recorded during this period yet.";
      return;
    }

    const maxSessions = Math.max(...stats.activity.map(bucket => bucket.sessions), 1);

    stats.activity.forEach(bucket => {
      const barContainer = document.createElement("div");
      barContainer.className = "stats-bar-item";

      const bar = document.createElement("div");
      bar.className = "stats-bar";

      if (bucket.sessions === 0) {
        bar.style.height = "0";
        bar.style.minHeight = "0";
      } else {
        bar.style.height = `${Math.max((bucket.sessions / maxSessions) * 100, 5)}%`;
      }

      bar.title = `${bucket.sessions} workout(s)`;

      const label = document.createElement("span");
      label.className = "stats-bar-label";
      const [year, month, day] = bucket.date.split("-").map(Number);
      const bucketDate = new Date(year, month - 1, day);
      label.textContent = period === "week"
        ? bucketDate.toLocaleDateString(undefined, { weekday: "short" })
        : bucketDate.toLocaleDateString(undefined, { month: "short" });

      const count = document.createElement("span");
      count.className = "stats-bar-count";
      count.textContent = bucket.sessions;

      barContainer.append(count, bar, label);
      chart.appendChild(barContainer);
    });

  } catch (error) {
    document.querySelector("#stats-chart").textContent =
      "Could not load statistics: " + error.message;
  }
}

document.querySelector("#stats-period").addEventListener("change", () => {
  loadStats(document.querySelector("#stats-period").value);
});

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

function renderLibraryFilterOptions(container, options, selectedValues) {
  container.replaceChildren(...options.map((option) => {
    const button = makeElement("button", "library-filter-chip", option.label);
    button.type = "button";
    button.setAttribute("aria-pressed", String(selectedValues.has(option.value)));
    button.classList.toggle("is-selected", selectedValues.has(option.value));
    button.addEventListener("click", () => {
      if (selectedValues.has(option.value)) selectedValues.delete(option.value);
      else selectedValues.add(option.value);
      button.classList.toggle("is-selected", selectedValues.has(option.value));
      button.setAttribute("aria-pressed", String(selectedValues.has(option.value)));
      filterLibraryExercises();
    });
    return button;
  }));
}

function renderLibraryExercise(exercise) {
  const card = makeElement("article", "library-exercise-card");
  card.dataset.exerciseId = String(exercise.id);
  card.append(createExerciseThumbnail(
    exercise,
    "library-exercise-media",
    "library-exercise-placeholder"
  ));
  card.append(makeElement("h3", "library-exercise-title", exercise.name));
  attachExercisePreview(card, exercise);
  return card;
}

function matchesLibraryEquipment(exercise) {
  if (selectedLibraryEquipment.size === 0) return true;

  const availableEquipment = new Set(
    [...selectedLibraryEquipment].filter((item) => item !== "__no_equipment__")
  );
  if (exercise.equipment.length === 0) {
    return availableEquipment.size > 0 || selectedLibraryEquipment.has("__no_equipment__");
  }
  return exercise.equipment.every((item) => availableEquipment.has(item));
}

function filterLibraryExercises() {
  const query = librarySearchInput.value.trim().toLowerCase();
  const filteredExercises = libraryExercises.filter((exercise) => {
    const matchesName = exercise.name.toLowerCase().includes(query);
    const matchesEquipment = matchesLibraryEquipment(exercise);
    const matchesTarget = selectedLibraryTargets.size === 0
      || [...selectedLibraryTargets].some((target) => (
        target === "cardio"
          ? exercise.type === "cardio"
          : exercise.body_area.includes(target)
      ));
    return matchesName && matchesEquipment && matchesTarget;
  });

  libraryResultCount.textContent = `${filteredExercises.length} ${
    filteredExercises.length === 1 ? "exercise" : "exercises"
  }`;
  closeExerciseHoverPreview();
  libraryExerciseGrid.replaceChildren(...filteredExercises.map(renderLibraryExercise));
  libraryEmpty.hidden = filteredExercises.length > 0;
}

async function loadLibrary() {
  if (libraryLoaded || libraryLoading) return;
  libraryLoading = true;
  libraryStatus.textContent = "Loading exercises…";
  try {
    const data = await requestJson("/api/library");
    libraryExercises = data.exercises;
    const equipmentOptions = data.equipment.map((item) => ({ value: item, label: prettyLabel(item) }));
    equipmentOptions.push({ value: "__no_equipment__", label: "No equipment" });
    renderLibraryFilterOptions(
      libraryEquipmentFilters,
      equipmentOptions,
      selectedLibraryEquipment
    );
    renderLibraryFilterOptions(
      libraryTargetFilters,
      data.targets.map((target) => ({
        value: target,
        label: target === "core" ? "Abs / Core" : prettyLabel(target),
      })),
      selectedLibraryTargets
    );
    libraryLoaded = true;
    libraryStatus.textContent = "";
    filterLibraryExercises();
  } catch (error) {
    libraryStatus.textContent = error.message;
  } finally {
    libraryLoading = false;
  }
}

async function loadActiveWorkout() {
  try {
    const data = await requestJson("/api/active-workout");
    if (data.active_workout) {
      renderActiveWorkout(data.active_workout);
    }
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

  closeExerciseHoverPreview();
  document.querySelectorAll(".app-page").forEach((section) => {
    section.hidden = section !== page;
  });
  appNav.querySelectorAll("[data-page-target]").forEach((link) => {
    const active = link.dataset.pageTarget === pageName;
    link.classList.toggle("is-active", active);
    if (active) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
  if (pageName === "tracker") {
  loadHistory();
  loadStats();
  loadPausedWorkouts();
}

if (pageName === "library") loadLibrary();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function setAuthMode(mode) {
  authMode = mode;
  const registering = mode === "register";
  signupNameFields.hidden = !registering;
  authFirstName.required = registering;
  authLastName.required = registering;
  if (registering) {
    authPassword.minLength = 8;
  } else {
    authPassword.removeAttribute("minlength");
  }
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
  await Promise.all([
    loadOptions(),
    loadHistory(),
    loadStats(),
    loadPausedWorkouts(),
  ]);
  await loadActiveWorkout();
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

librarySearchInput.addEventListener("input", filterLibraryExercises);

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
    currentGoal = "";
    currentLevel = "";
    currentEquipment = [];
    currentExercises = [];
    currentDuration = 0;
    currentRecommendationSeed = null;
    workoutSteps = [];
    currentWorkoutStepIndex = 0;
    currentWorkoutSessionId = null;
    completedWorkoutSteps.clear();
    closeWorkoutSheet();
    finishWorkoutButton.hidden = true;
    workoutCompletionOverlay.hidden = true;
    workoutSheetPanel.classList.remove("workout-complete");
    workoutSection.hidden = true;
    workoutActions.hidden = true;
    startButton.hidden = true;
    saveAndClearButton.hidden = true;
    continueWorkoutButton.hidden = true;
    closeExerciseHoverPreview();
    exerciseList.replaceChildren();
    activeWorkoutMessage.textContent = "";
    historyList.replaceChildren(makeElement("p", "field-hint", "Log in to see your saved workouts."));
    pausedWorkoutList.replaceChildren();
    pausedWorkoutSection.hidden = true;
    pausedWorkoutMessage.textContent = "";
    setAuthMode("login");
  } catch (error) {
    historyMessage.textContent = error.message;
  } finally {
    logoutButton.disabled = false;
  }
});

plannerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  plannerMessage.textContent = "";
  if (!goalSelect.value) {
    plannerMessage.textContent = "Choose a fitness goal to build your workout.";
    goalTrigger.focus();
    return;
  }
  recommendButton.disabled = true;
  try {
    if (!skipWorkoutConflictCheck) {
      if (currentWorkoutSessionId) {
        promptToReplaceWorkout("create", {
          session_id: currentWorkoutSessionId,
          structure_mode: currentWorkoutStructureMode,
          completed_set_keys: [...completedWorkoutSteps],
          notes: currentWorkoutNotes,
        });
        return;
      }
      const active = await requestJson("/api/active-workout");
      if (active.active_workout) {
        promptToReplaceWorkout("create", active.active_workout);
        return;
      }
      const paused = await requestJson("/api/paused-workouts");
      if (paused.paused_workouts.length > 0) {
        promptToReplaceWorkout("create", null);
        return;
      }
    }
    skipWorkoutConflictCheck = false;

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
    if (!data.exercises.length) {
      renderEmptyWorkout(goalSelect.value, level, duration, data.empty_message);
      return;
    }
    currentGoal = goalSelect.value;
    currentLevel = level;
    currentEquipment = [...equipmentOptions.querySelectorAll("input:checked")]
      .map((input) => input.value);
    currentExercises = data.exercises;
    currentDuration = duration;
    currentRecommendationSeed = data.recommendation_seed;
    workoutSteps = [];
    currentWorkoutStepIndex = 0;
    completedWorkoutSteps.clear();
    document.querySelector("#workout-focus").textContent = prettyLabel(currentGoal);
    document.querySelector("#workout-level").textContent = prettyLabel(level);
    document.querySelector("#workout-duration").textContent = `${duration} minutes`;
    workoutActions.hidden = false;
    startButton.hidden = false;
    saveAndClearButton.hidden = true;
    continueWorkoutButton.hidden = true;
    document.querySelector("#no-results").hidden = true;
    workoutSection.hidden = false;
    activeWorkoutMessage.textContent = "";
    renderExercises();
    workoutSection.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    plannerMessage.textContent = error.message;
  } finally {
    skipWorkoutConflictCheck = false;
    recommendButton.disabled = !goalSelect.value;
  }
});

async function startActiveWorkoutFromPlan() {
  const data = await requestJson("/api/active-workout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      goal: currentGoal,
      level: currentLevel,
      equipment: currentEquipment,
      duration: currentDuration,
      recommendation_seed: currentRecommendationSeed,
    }),
  });
  if (!data.active_workout) {
    plannerMessage.textContent = data.empty_message;
    return;
  }
  renderActiveWorkout(data.active_workout);
  openWorkoutSheet();
}

cancelNewWorkoutButton.addEventListener("click", () => {
  newWorkoutConfirmDialog.close();
});

newWorkoutConfirmDialog.addEventListener("close", () => {
  pendingNewWorkoutAction = null;
  pendingWorkoutToPause = null;
  newWorkoutConfirmTitle.textContent = "Start a new workout?";
  confirmNewWorkoutButton.textContent = "Yes, save and create new";
});

newWorkoutConfirmDialog.addEventListener("click", (event) => {
  if (event.target === newWorkoutConfirmDialog && !confirmNewWorkoutButton.disabled) {
    newWorkoutConfirmDialog.close();
  }
});

newWorkoutConfirmDialog.addEventListener("cancel", (event) => {
  if (confirmNewWorkoutButton.disabled) event.preventDefault();
});

confirmNewWorkoutButton.addEventListener("click", async () => {
  confirmNewWorkoutButton.disabled = true;
  cancelNewWorkoutButton.disabled = true;
  const pendingAction = pendingNewWorkoutAction;
  const workout = pendingWorkoutToPause;
  newWorkoutConfirmMessage.textContent = workout ? "Saving your current workout..." : "";
  try {
    if (!pendingAction) throw new Error("The requested workout action is unavailable.");
    if (workout) {
      await pauseWorkout(workout);
      if (workout.session_id === currentWorkoutSessionId) hideGeneratedWorkout();
    }
  } catch (error) {
    newWorkoutConfirmMessage.textContent = error.message;
    confirmNewWorkoutButton.disabled = false;
    cancelNewWorkoutButton.disabled = false;
    return;
  }

  await loadPausedWorkouts();
  newWorkoutConfirmDialog.close();
  confirmNewWorkoutButton.disabled = false;
  cancelNewWorkoutButton.disabled = false;
  if (pendingAction.action === "create") {
    hideGeneratedWorkout();
    skipWorkoutConflictCheck = true;
    plannerForm.requestSubmit();
  } else if (pendingAction.action === "start") {
    startButton.disabled = true;
    try {
      await startActiveWorkoutFromPlan();
    } catch (error) {
      plannerMessage.textContent = error.message;
    } finally {
      startButton.disabled = false;
    }
  } else if (pendingAction.action === "resume") {
    try {
      await resumeSavedWorkout(pendingAction.sessionId);
    } catch (error) {
      pausedWorkoutMessage.textContent = error.message;
    }
  } else if (pendingAction.action === "redo") {
    try {
      await redoSavedWorkout(pendingAction.sessionId);
    } catch (error) {
      historyMessage.textContent = error.message;
    }
  }
});

startButton.addEventListener("click", async () => {
  startButton.disabled = true;
  plannerMessage.textContent = "";
  try {
    const active = await requestJson("/api/active-workout");
    if (active.active_workout) {
      promptToReplaceWorkout("start", active.active_workout);
      return;
    }
    await startActiveWorkoutFromPlan();
  } catch (error) {
    if (error.status === 409) {
      try {
        const active = await requestJson("/api/active-workout");
        if (active.active_workout) {
          promptToReplaceWorkout("start", active.active_workout);
          return;
        }
      } catch (activeWorkoutError) {
        plannerMessage.textContent = activeWorkoutError.message;
        return;
      }
    }
    plannerMessage.textContent = error.message;
  } finally {
    startButton.disabled = false;
  }
});

continueWorkoutButton.addEventListener("click", openWorkoutSheet);

saveAndClearButton.addEventListener("click", async () => {
  if (!currentWorkoutSessionId) {
    plannerMessage.textContent = "There is no active workout to save.";
    return;
  }

  saveAndClearButton.disabled = true;
  saveAndClearButton.textContent = "Saving...";
  plannerMessage.textContent = "";
  try {
    await pauseWorkout({
      session_id: currentWorkoutSessionId,
      structure_mode: currentWorkoutStructureMode,
      completed_set_keys: [...completedWorkoutSteps],
      notes: currentWorkoutNotes,
    });
    hideGeneratedWorkout();
    document.querySelector("#planner-title").focus();
    await loadPausedWorkouts();
  } catch (error) {
    plannerMessage.textContent = error.message;
  } finally {
    saveAndClearButton.disabled = false;
    saveAndClearButton.textContent = "Save and clear";
  }
});

checkSession();
