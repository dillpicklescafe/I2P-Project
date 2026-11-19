exercises = [
    # UPPER BODY
    {
        "id": 1,
        "name": "Wall Push-up",
        "body_area": ["chest", "triceps"],
        "goals": ["first_pushup", "upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "push",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand facing a wall.",
            "Place both hands against the wall.",
            "Bend your elbows and move your chest toward the wall.",
            "Push yourself back to the starting position."
        ],
        "easier_variation": None,
        "harder_variation": "Incline Push-up"
    },

    {
        "id": 2,
        "name": "Incline Push-up",
        "body_area": ["chest", "triceps"],
        "goals": ["first_pushup", "upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["bench"],
        "movement_type": "push",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Place your hands on a stable elevated surface.",
            "Keep your body in a straight line.",
            "Bend your elbows and lower your chest.",
            "Push back to the starting position."
        ],
        "easier_variation": "Wall Push-up",
        "harder_variation": "Knee Push-up"
    },

    {
        "id": 3,
        "name": "Knee Push-up",
        "body_area": ["chest", "triceps", "shoulders"],
        "goals": ["first_pushup", "upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "push",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Start on your hands and knees.",
            "Keep your body aligned from your knees to your head.",
            "Bend your elbows to lower your chest.",
            "Push back up."
        ],
        "easier_variation": "Wall Push-up",
        "harder_variation": "Regular Push-up"
    },

    {
        "id": 4,
        "name": "Regular Push-up",
        "body_area": ["chest", "triceps", "shoulders"],
        "goals": ["upper_body_strength", "first_pushup"],
        "type": "strength",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "push",
        "sets": 3,
        "reps": 8,
        "hold_seconds": None,
        "duration": 5,
        "instructions": [
            "Start in a high plank position.",
            "Keep your body in a straight line.",
            "Bend your elbows and lower your chest.",
            "Push back up while keeping your body aligned."
        ],
        "easier_variation": "Knee Push-up",
        "harder_variation": None
    },

    {
        "id": 5,
        "name": "Dumbbell Shoulder Press",
        "body_area": ["shoulders", "triceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["dumbbells"],
        "movement_type": "push",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Sit upright while holding a dumbbell in each hand.",
            "Start with your hands near shoulder level.",
            "Press the weights upward comfortably.",
            "Lower them slowly."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    # BACK

    {
        "id": 6,
        "name": "Dumbbell Row",
        "body_area": ["back", "biceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Hold a dumbbell in each hand.",
            "Hinge forward slightly with a stable back.",
            "Pull your elbows toward your body.",
            "Lower the dumbbells slowly."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 7,
        "name": "Resistance Band Row",
        "body_area": ["back", "biceps"],
        "goals": ["upper_body_strength", "posture"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["resistance_band"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Sit with your legs comfortably extended.",
            "Hold the resistance band securely.",
            "Pull your elbows backward.",
            "Return slowly to the starting position."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 8,
        "name": "Bird Dog",
        "body_area": ["back", "core"],
        "goals": ["core_stability", "balance"],
        "type": "stability",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "stability",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Start on your hands and knees.",
            "Extend one arm and the opposite leg.",
            "Keep your back stable.",
            "Return and repeat on the other side."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    # ARMS

    {
        "id": 9,
        "name": "Biceps Curl",
        "body_area": ["biceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand while holding dumbbells.",
            "Keep your elbows close to your body.",
            "Bend your elbows to lift the weights.",
            "Lower the weights slowly."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 10,
        "name": "Triceps Kickback",
        "body_area": ["triceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "push",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Hold a dumbbell in each hand.",
            "Lean forward slightly with a stable back.",
            "Keep your upper arms close to your body.",
            "Straighten your elbows and return slowly."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    # LOWER BODY

    {
        "id": 11,
        "name": "Bodyweight Squat",
        "body_area": ["quads", "glutes"],
        "goals": ["lower_body_strength", "overall_fitness"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "squat",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand with your feet about shoulder-width apart.",
            "Bend your knees and hips.",
            "Lower yourself comfortably.",
            "Stand back up."
        ],
        "easier_variation": "Chair Squat",
        "harder_variation": "Goblet Squat"
    },

    {
        "id": 12,
        "name": "Chair Squat",
        "body_area": ["quads", "glutes"],
        "goals": ["lower_body_strength", "accessibility"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["chair"],
        "movement_type": "squat",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand in front of a stable chair.",
            "Bend your knees and hips.",
            "Lower yourself toward the chair.",
            "Stand up again."
        ],
        "easier_variation": None,
        "harder_variation": "Bodyweight Squat"
    },

    {
        "id": 13,
        "name": "Glute Bridge",
        "body_area": ["glutes", "hamstrings"],
        "goals": ["lower_body_strength", "core_stability"],
        "type": "strength",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "hinge",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Lie on your back with your knees bent.",
            "Keep your feet flat on the floor.",
            "Lift your hips comfortably.",
            "Lower your hips slowly."
        ],
        "easier_variation": None,
        "harder_variation": "Single-leg Glute Bridge"
    },

    {
        "id": 14,
        "name": "Reverse Lunge",
        "body_area": ["quads", "glutes"],
        "goals": ["lower_body_strength", "balance"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "lunge",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand upright with your feet together.",
            "Step one foot backward.",
            "Bend both knees comfortably.",
            "Return to standing and switch sides."
        ],
        "easier_variation": "Supported Reverse Lunge",
        "harder_variation": None
    },

    {
        "id": 15,
        "name": "Calf Raise",
        "body_area": ["calves"],
        "goals": ["lower_body_strength", "balance"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "raise",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand with your feet hip-width apart.",
            "Raise your heels off the floor.",
            "Pause briefly at the top.",
            "Lower your heels slowly."
        ],
        "easier_variation": "Seated Calf Raise",
        "harder_variation": None
    },

    {
        "id": 16,
        "name": "Clamshell",
        "body_area": ["glutes", "hips"],
        "goals": ["hip_stability", "lower_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "lying",
        "equipment": [],
        "movement_type": "abduction",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Lie on your side with your knees bent.",
            "Keep your feet together.",
            "Lift your upper knee without rolling your hips.",
            "Lower your knee slowly and repeat."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    # CORE

    {
        "id": 17,
        "name": "Plank",
        "body_area": ["core", "shoulders"],
        "goals": ["core_stability", "overall_fitness"],
        "type": "stability",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "hold",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 2,
        "instructions": [
            "Start on your forearms and toes.",
            "Keep your body in a straight line.",
            "Engage your abdominal muscles.",
            "Hold the position while breathing normally."
        ],
        "easier_variation": "Knee Plank",
        "harder_variation": None
    },

    {
        "id": 18,
        "name": "Knee Plank",
        "body_area": ["core"],
        "goals": ["core_stability", "first_pushup"],
        "type": "stability",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "hold",
        "sets": 2,
        "reps": None,
        "hold_seconds": 15,
        "duration": 2,
        "instructions": [
            "Start on your forearms and knees.",
            "Keep your body aligned from your knees to your head.",
            "Engage your core.",
            "Hold while breathing normally."
        ],
        "easier_variation": None,
        "harder_variation": "Plank"
    },

    {
        "id": 19,
        "name": "Dead Bug",
        "body_area": ["core"],
        "goals": ["core_stability"],
        "type": "stability",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "stability",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Lie on your back with your arms raised.",
            "Bend your knees to about 90 degrees.",
            "Lower one arm and the opposite leg slowly.",
            "Return and switch sides."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 20,
        "name": "Seated Knee Lift",
        "body_area": ["core", "hip_flexors"],
        "goals": ["core_stability", "accessibility"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["chair"],
        "movement_type": "lift",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Sit upright on a stable chair.",
            "Keep your feet on the floor.",
            "Lift one knee comfortably.",
            "Lower it and repeat with the other knee."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    # ======================================
    # CARDIO
    # ======================================

    {
        "id": 21,
        "name": "Marching in Place",
        "body_area": ["legs", "full_body"],
        "goals": ["cardio", "warm_up"],
        "type": "cardio",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "march",
        "sets": 1,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand upright.",
            "Lift one knee and then the other.",
            "Swing your arms naturally.",
            "Continue at a comfortable pace."
        ],
        "easier_variation": "Seated Marching",
        "harder_variation": None
    },

    {
        "id": 22,
        "name": "Seated Marching",
        "body_area": ["legs"],
        "goals": ["cardio", "accessibility"],
        "type": "cardio",
        "level": "beginner",
        "position": "seated",
        "equipment": ["chair"],
        "movement_type": "march",
        "sets": 1,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Sit upright on a stable chair.",
            "Lift one knee at a time.",
            "Move your arms naturally if comfortable.",
            "Continue at a comfortable pace."
        ],
        "easier_variation": None,
        "harder_variation": "Marching in Place"
    },

    {
        "id": 23,
        "name": "Step Touch",
        "body_area": ["legs"],
        "goals": ["cardio", "coordination"],
        "type": "cardio",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "step",
        "sets": 1,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand with your feet together.",
            "Step to one side.",
            "Bring the other foot toward it.",
            "Repeat in the opposite direction."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 24,
        "name": "Low-impact Jumping Jack",
        "body_area": ["full_body", "legs"],
        "goals": ["cardio", "overall_fitness"],
        "type": "cardio",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "cardio",
        "sets": 1,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand with your feet together.",
            "Step one foot out while raising your arms.",
            "Return to the starting position.",
            "Repeat on the other side."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    # BALANCE

    {
        "id": 25,
        "name": "Supported Single-leg Balance",
        "body_area": ["legs", "core"],
        "goals": ["balance", "coordination"],
        "type": "balance",
        "level": "beginner",
        "position": "standing",
        "equipment": ["chair"],
        "movement_type": "balance",
        "sets": 2,
        "reps": None,
        "hold_seconds": 10,
        "duration": 2,
        "instructions": [
            "Stand beside a stable chair.",
            "Hold the chair for support.",
            "Lift one foot slightly off the floor.",
            "Return your foot and switch sides."
        ],
        "easier_variation": None,
        "harder_variation": "Single-leg Balance"
    },

    {
        "id": 26,
        "name": "Tandem Stance",
        "body_area": ["legs", "core"],
        "goals": ["balance", "coordination"],
        "type": "balance",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "balance",
        "sets": 2,
        "reps": None,
        "hold_seconds": 15,
        "duration": 2,
        "instructions": [
            "Stand near a stable support.",
            "Place one foot directly in front of the other.",
            "Keep your balance comfortably.",
            "Switch which foot is in front."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    # MOBILITY AND FLEXIBILITY

    {
        "id": 27,
        "name": "Arm Circles",
        "body_area": ["shoulders"],
        "goals": ["mobility", "warm_up"],
        "type": "mobility",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "mobility",
        "sets": 1,
        "reps": 10,
        "hold_seconds": None,
        "duration": 2,
        "instructions": [
            "Stand comfortably with your arms extended.",
            "Make small circles with your arms.",
            "Gradually make the circles larger if comfortable.",
            "Change direction."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 28,
        "name": "Cat-Cow",
        "body_area": ["back", "core"],
        "goals": ["mobility", "warm_up"],
        "type": "mobility",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "mobility",
        "sets": 1,
        "reps": 8,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Start on your hands and knees.",
            "Gently round your back upward.",
            "Slowly move your back in the opposite direction.",
            "Move smoothly with your breathing."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 29,
        "name": "Standing Calf Stretch",
        "body_area": ["calves"],
        "goals": ["mobility", "cool_down"],
        "type": "flexibility",
        "level": "beginner",
        "position": "standing",
        "equipment": ["wall"],
        "movement_type": "stretch",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 2,
        "instructions": [
            "Stand facing a wall.",
            "Place your hands on the wall for support.",
            "Step one foot backward and keep its heel down.",
            "Hold gently and switch sides."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 30,
        "name": "Cross-body Shoulder Stretch",
        "body_area": ["shoulders"],
        "goals": ["mobility", "cool_down"],
        "type": "flexibility",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "stretch",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 2,
        "instructions": [
            "Bring one arm across your chest.",
            "Use your other arm to support it gently.",
            "Hold the stretch comfortably.",
            "Switch arms."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    # ======================================
    # UPPER BODY (ADDITIONAL: ID 31 - 45)
    # ======================================

    {
        "id": 31,
        "name": "Wide Push-up",
        "body_area": ["chest", "shoulders", "triceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "push",
        "sets": 3,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Start in a high plank with hands placed wider than shoulder-width.",
            "Keep your core engaged and body straight.",
            "Lower your chest toward the floor.",
            "Push back up to the starting position."
        ],
        "easier_variation": "Regular Push-up",
        "harder_variation": "Decline Push-up"
    },

    {
        "id": 32,
        "name": "Decline Push-up",
        "body_area": ["chest", "shoulders", "triceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "advanced",
        "position": "floor",
        "equipment": ["bench"],
        "movement_type": "push",
        "sets": 3,
        "reps": 8,
        "hold_seconds": None,
        "duration": 5,
        "instructions": [
            "Place your feet on a stable bench and hands on the floor.",
            "Keep your body aligned from head to heels.",
            "Bend your elbows to lower your chest toward the floor.",
            "Press back up with control."
        ],
        "easier_variation": "Regular Push-up",
        "harder_variation": None
    },

    {
        "id": 33,
        "name": "Dumbbell Bench Press",
        "body_area": ["chest", "triceps", "shoulders"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "lying",
        "equipment": ["dumbbells", "bench"],
        "movement_type": "push",
        "sets": 3,
        "reps": 10,
        "hold_seconds": None,
        "duration": 5,
        "instructions": [
            "Lie flat on a bench holding a dumbbell in each hand.",
            "Position the dumbbells near chest level.",
            "Press the weights upward until your arms are extended.",
            "Lower the dumbbells slowly back to chest level."
        ],
        "easier_variation": "Dumbbell Floor Press",
        "harder_variation": "Incline Dumbbell Press"
    },

    {
        "id": 34,
        "name": "Dumbbell Floor Press",
        "body_area": ["chest", "triceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "floor",
        "equipment": ["dumbbells"],
        "movement_type": "push",
        "sets": 3,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Lie on your back with your knees bent and feet flat.",
            "Hold a dumbbell in each hand with upper arms on the floor.",
            "Press the weights straight up over your chest.",
            "Lower slowly until your upper arms touch the floor."
        ],
        "easier_variation": None,
        "harder_variation": "Dumbbell Bench Press"
    },

    {
        "id": 35,
        "name": "Dumbbell Chest Fly",
        "body_area": ["chest", "shoulders"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "lying",
        "equipment": ["dumbbells", "bench"],
        "movement_type": "fly",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Lie on a bench holding dumbbells above your chest.",
            "Keep a slight bend in your elbows.",
            "Open your arms out to the sides comfortably.",
            "Bring the dumbbells back together above your chest."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 36,
        "name": "Standing Dumbbell Shoulder Press",
        "body_area": ["shoulders", "triceps"],
        "goals": ["upper_body_strength", "core_stability"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "push",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand tall with feet shoulder-width apart holding dumbbells.",
            "Bring the weights to shoulder height.",
            "Press the dumbbells overhead without arching your back.",
            "Lower them slowly to shoulder level."
        ],
        "easier_variation": "Dumbbell Shoulder Press",
        "harder_variation": "Arnold Press"
    },

    {
        "id": 37,
        "name": "Dumbbell Lateral Raise",
        "body_area": ["shoulders"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "raise",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand upright holding dumbbells at your sides.",
            "Keep a slight bend in your elbows.",
            "Raise your arms out to the sides until shoulder height.",
            "Lower the weights slowly with control."
        ],
        "easier_variation": "Resistance Band Lateral Raise",
        "harder_variation": None
    },

    {
        "id": 38,
        "name": "Dumbbell Front Raise",
        "body_area": ["shoulders"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "raise",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand tall holding dumbbells in front of your thighs.",
            "Keep your arms straight with a soft elbow bend.",
            "Lift the weights forward to shoulder height.",
            "Lower them back down slowly."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 39,
        "name": "Pike Push-up",
        "body_area": ["shoulders", "triceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "push",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Start in a downward-facing V shape with hips lifted.",
            "Keep your hands shoulder-width apart on the floor.",
            "Bend your elbows to lower the top of your head toward the floor.",
            "Push back up to the starting position."
        ],
        "easier_variation": "Incline Push-up",
        "harder_variation": None
    },

    {
        "id": 40,
        "name": "Resistance Band Chest Press",
        "body_area": ["chest", "triceps", "shoulders"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["resistance_band"],
        "movement_type": "push",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Wrap a resistance band behind your upper back.",
            "Hold both ends near chest level.",
            "Press your hands forward until your arms are straight.",
            "Return slowly to the starting position."
        ],
        "easier_variation": "Wall Push-up",
        "harder_variation": "Regular Push-up"
    },

    {
        "id": 41,
        "name": "Resistance Band Shoulder Press",
        "body_area": ["shoulders", "triceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["resistance_band"],
        "movement_type": "push",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand on the center of a resistance band.",
            "Hold the handles at shoulder height.",
            "Press your hands overhead smoothly.",
            "Lower back to shoulder level with control."
        ],
        "easier_variation": None,
        "harder_variation": "Standing Dumbbell Shoulder Press"
    },

    {
        "id": 42,
        "name": "Arnold Press",
        "body_area": ["shoulders", "triceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "intermediate",
        "position": "seated",
        "equipment": ["dumbbells"],
        "movement_type": "push",
        "sets": 3,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Sit upright holding dumbbells in front of your shoulders with palms facing you.",
            "Rotate your palms forward as you press the weights overhead.",
            "Extend your arms comfortably at the top.",
            "Reverse the motion slowly to return to the start."
        ],
        "easier_variation": "Dumbbell Shoulder Press",
        "harder_variation": None
    },

    {
        "id": 43,
        "name": "Scapular Push-up",
        "body_area": ["shoulders", "chest", "core"],
        "goals": ["upper_body_strength", "posture", "first_pushup"],
        "type": "stability",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "push",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Start in a high plank or tabletop position with straight arms.",
            "Keep your elbows locked as you pinch your shoulder blades together.",
            "Push the floor away to spread your shoulder blades apart.",
            "Repeat with slow, controlled movements."
        ],
        "easier_variation": None,
        "harder_variation": "Regular Push-up"
    },

    {
        "id": 44,
        "name": "Incline Dumbbell Press",
        "body_area": ["chest", "shoulders", "triceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "intermediate",
        "position": "seated",
        "equipment": ["dumbbells", "bench"],
        "movement_type": "push",
        "sets": 3,
        "reps": 10,
        "hold_seconds": None,
        "duration": 5,
        "instructions": [
            "Lie back on an incline bench holding a dumbbell in each hand.",
            "Start with the weights at upper-chest level.",
            "Press the dumbbells upward until your arms are extended.",
            "Lower them slowly back to the starting position."
        ],
        "easier_variation": "Dumbbell Bench Press",
        "harder_variation": None
    },

    {
        "id": 45,
        "name": "Resistance Band Lateral Raise",
        "body_area": ["shoulders"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["resistance_band"],
        "movement_type": "raise",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand on a resistance band holding the ends at your sides.",
            "Keep your torso upright and elbows slightly bent.",
            "Raise your arms out to the sides to shoulder height.",
            "Lower your arms slowly back down."
        ],
        "easier_variation": None,
        "harder_variation": "Dumbbell Lateral Raise"
    },

    # ======================================
    # BACK (ADDITIONAL: ID 46 - 60)
    # ======================================

    {
        "id": 46,
        "name": "Single-arm Dumbbell Row",
        "body_area": ["back", "biceps"],
        "goals": ["upper_body_strength", "posture"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["dumbbells", "bench"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Place one hand and knee on a bench for support.",
            "Hold a dumbbell in your free hand with arm extended.",
            "Pull the dumbbell toward your hip while keeping your back flat.",
            "Lower slowly and switch sides after completing your reps."
        ],
        "easier_variation": "Resistance Band Row",
        "harder_variation": None
    },

    {
        "id": 47,
        "name": "Superman Hold",
        "body_area": ["back", "glutes"],
        "goals": ["core_stability", "posture"],
        "type": "stability",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "hold",
        "sets": 2,
        "reps": None,
        "hold_seconds": 15,
        "duration": 3,
        "instructions": [
            "Lie face down on the floor with arms extended overhead.",
            "Gently lift your chest, arms, and legs off the floor.",
            "Keep your neck neutral and gaze downward.",
            "Hold the position comfortably while breathing steadily."
        ],
        "easier_variation": "Prone Cobra Hold",
        "harder_variation": "Superman Lift"
    },

    {
        "id": 48,
        "name": "Superman Lift",
        "body_area": ["back", "glutes"],
        "goals": ["upper_body_strength", "posture"],
        "type": "strength",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "lift",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Lie face down with arms extended forward and legs straight.",
            "Lift your arms, chest, and legs a few inches off the floor.",
            "Pause briefly at the top.",
            "Lower back down slowly and repeat."
        ],
        "easier_variation": "Superman Hold",
        "harder_variation": None
    },

    {
        "id": 49,
        "name": "Reverse Snow Angel",
        "body_area": ["back", "shoulders"],
        "goals": ["posture", "upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "raise",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Lie face down with your forehead resting lightly on a folded towel.",
            "Lift your arms slightly off the floor at your sides.",
            "Sweep your arms overhead in a wide arc.",
            "Return your arms to your sides with control."
        ],
        "easier_variation": None,
        "harder_variation": "Prone Y-T-W Raise"
    },

    {
        "id": 50,
        "name": "Bent-over Reverse Fly",
        "body_area": ["back", "shoulders"],
        "goals": ["upper_body_strength", "posture"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "fly",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Hold a light dumbbell in each hand and hinge forward at the hips.",
            "Keep your back flat and elbows slightly bent.",
            "Raise your arms out to the sides, squeezing your shoulder blades.",
            "Lower the weights slowly."
        ],
        "easier_variation": "Resistance Band Pull-apart",
        "harder_variation": None
    },

    {
        "id": 51,
        "name": "Resistance Band Lat Pulldown",
        "body_area": ["back", "biceps"],
        "goals": ["upper_body_strength", "posture"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["resistance_band"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Hold a resistance band overhead with hands wider than shoulder-width.",
            "Sit tall with your chest lifted.",
            "Pull the band downward toward your upper chest while widening your hands.",
            "Return slowly to the overhead position."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 52,
        "name": "Resistance Band Face Pull",
        "body_area": ["back", "shoulders"],
        "goals": ["posture", "upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["resistance_band"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Anchor a resistance band at chest or eye level.",
            "Hold both ends with palms facing each other.",
            "Pull the band toward your forehead while keeping elbows high.",
            "Return slowly to the starting position."
        ],
        "easier_variation": "Resistance Band Pull-apart",
        "harder_variation": None
    },

    {
        "id": 53,
        "name": "Resistance Band Pull-apart",
        "body_area": ["back", "shoulders"],
        "goals": ["posture", "warm_up"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["resistance_band"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand tall holding a resistance band straight in front of your chest.",
            "Keep your arms extended at shoulder height.",
            "Pull the band apart until it touches your chest.",
            "Return slowly to the starting position."
        ],
        "easier_variation": None,
        "harder_variation": "Bent-over Reverse Fly"
    },

    {
        "id": 54,
        "name": "Prone Y-T-W Raise",
        "body_area": ["back", "shoulders"],
        "goals": ["posture", "upper_body_strength"],
        "type": "strength",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "raise",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Lie face down on the floor with arms extended overhead in a Y shape.",
            "Lift your arms briefly, then move them out into a T shape and lift.",
            "Bend your elbows into a W shape and squeeze your shoulder blades.",
            "Lower with control and repeat the sequence."
        ],
        "easier_variation": "Reverse Snow Angel",
        "harder_variation": None
    },

    {
        "id": 55,
        "name": "Renegade Row",
        "body_area": ["back", "core", "biceps"],
        "goals": ["upper_body_strength", "core_stability"],
        "type": "strength",
        "level": "intermediate",
        "position": "floor",
        "equipment": ["dumbbells"],
        "movement_type": "pull",
        "sets": 3,
        "reps": 8,
        "hold_seconds": None,
        "duration": 5,
        "instructions": [
            "Start in a high plank holding a dumbbell in each hand.",
            "Keep your feet wide and hips steady.",
            "Pull one dumbbell toward your ribs while balancing on the other hand.",
            "Lower the dumbbell and alternate sides."
        ],
        "easier_variation": "Dumbbell Row",
        "harder_variation": None
    },

    {
        "id": 56,
        "name": "Inverted Row",
        "body_area": ["back", "biceps", "core"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "intermediate",
        "position": "lying",
        "equipment": ["bar"],
        "movement_type": "pull",
        "sets": 3,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Lie beneath a sturdy low bar and grip it wider than shoulder-width.",
            "Keep your body straight from heels to head.",
            "Pull your chest up toward the bar.",
            "Lower yourself back down with control."
        ],
        "easier_variation": "Resistance Band Row",
        "harder_variation": None
    },

    {
        "id": 57,
        "name": "Dumbbell Shrug",
        "body_area": ["back", "shoulders"],
        "goals": ["upper_body_strength", "posture"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "lift",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand upright holding dumbbells at your sides.",
            "Keep your arms straight and neck relaxed.",
            "Lift your shoulders straight up toward your ears.",
            "Lower your shoulders slowly."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 58,
        "name": "Chest-supported Dumbbell Row",
        "body_area": ["back", "biceps"],
        "goals": ["upper_body_strength", "posture"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["dumbbells", "bench"],
        "movement_type": "pull",
        "sets": 3,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Lie face down on an incline bench holding a dumbbell in each hand.",
            "Let your arms hang straight down toward the floor.",
            "Pull both elbows upward, squeezing your shoulder blades.",
            "Lower the dumbbells slowly."
        ],
        "easier_variation": "Resistance Band Row",
        "harder_variation": "Dumbbell Row"
    },

    {
        "id": 59,
        "name": "Prone Cobra Hold",
        "body_area": ["back", "shoulders"],
        "goals": ["posture", "core_stability"],
        "type": "stability",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "hold",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 3,
        "instructions": [
            "Lie face down with your arms at your sides and palms facing down.",
            "Gently lift your chest and hands off the floor.",
            "Draw your shoulder blades back and down.",
            "Hold while breathing smoothly."
        ],
        "easier_variation": None,
        "harder_variation": "Superman Hold"
    },

    {
        "id": 60,
        "name": "Good Morning",
        "body_area": ["back", "hamstrings", "glutes"],
        "goals": ["posture", "lower_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "hinge",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand with feet hip-width apart and hands lightly behind your head.",
            "Keep a slight bend in your knees and a flat back.",
            "Hinge forward at the hips until your torso is nearly parallel to the floor.",
            "Drive your hips forward to return to standing."
        ],
        "easier_variation": None,
        "harder_variation": "Dumbbell Romanian Deadlift"
    },

    # ======================================
    # ARMS (ADDITIONAL: ID 61 - 75)
    # ======================================

    {
        "id": 61,
        "name": "Hammer Curl",
        "body_area": ["biceps", "forearms"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand upright holding dumbbells with palms facing your sides.",
            "Keep your elbows tucked close to your torso.",
            "Curl the weights upward while keeping your palms facing inward.",
            "Lower the dumbbells slowly."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 62,
        "name": "Seated Biceps Curl",
        "body_area": ["biceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["dumbbells"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Sit upright on a chair or bench holding a dumbbell in each hand.",
            "Keep your upper arms steady at your sides.",
            "Bend your elbows to curl the weights toward your shoulders.",
            "Lower the weights slowly."
        ],
        "easier_variation": None,
        "harder_variation": "Biceps Curl"
    },

    {
        "id": 63,
        "name": "Concentration Curl",
        "body_area": ["biceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["dumbbells"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Sit on a bench with your legs apart and hold a dumbbell in one hand.",
            "Rest the back of your upper arm against your inner thigh.",
            "Curl the dumbbell upward toward your shoulder.",
            "Lower slowly and switch arms after finishing the set."
        ],
        "easier_variation": "Seated Biceps Curl",
        "harder_variation": None
    },

    {
        "id": 64,
        "name": "Alternating Dumbbell Curl",
        "body_area": ["biceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand tall holding a dumbbell in each hand at your sides.",
            "Curl one dumbbell upward while keeping the other arm straight.",
            "Lower the weight with control.",
            "Repeat with the opposite arm."
        ],
        "easier_variation": "Seated Biceps Curl",
        "harder_variation": "Zottman Curl"
    },

    {
        "id": 65,
        "name": "Resistance Band Biceps Curl",
        "body_area": ["biceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["resistance_band"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand on the middle of a resistance band with feet shoulder-width apart.",
            "Hold the handles with palms facing forward.",
            "Bend your elbows to curl your hands toward your shoulders.",
            "Lower your hands slowly to the starting position."
        ],
        "easier_variation": None,
        "harder_variation": "Biceps Curl"
    },

    {
        "id": 66,
        "name": "Overhead Triceps Extension",
        "body_area": ["triceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["dumbbells"],
        "movement_type": "push",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Sit upright holding one dumbbell with both hands overhead.",
            "Keep your elbows pointed forward and close to your head.",
            "Bend your elbows to lower the dumbbell behind your head.",
            "Straighten your arms to press the weight back up."
        ],
        "easier_variation": "Triceps Kickback",
        "harder_variation": None
    },

    {
        "id": 67,
        "name": "Lying Triceps Extension",
        "body_area": ["triceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "intermediate",
        "position": "floor",
        "equipment": ["dumbbells"],
        "movement_type": "push",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Lie on your back holding dumbbells straight above your shoulders.",
            "Keep your upper arms vertical and steady.",
            "Bend your elbows to lower the dumbbells beside your head.",
            "Extend your elbows to return to the start."
        ],
        "easier_variation": "Triceps Kickback",
        "harder_variation": None
    },

    {
        "id": 68,
        "name": "Chair Triceps Dip",
        "body_area": ["triceps", "shoulders"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["chair"],
        "movement_type": "push",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Sit on the edge of a sturdy chair and grip the front edge beside your hips.",
            "Slide your hips forward off the chair with knees bent.",
            "Bend your elbows to lower your body slightly.",
            "Push through your palms to return to the top."
        ],
        "easier_variation": "Resistance Band Triceps Pushdown",
        "harder_variation": "Bench Triceps Dip"
    },

    {
        "id": 69,
        "name": "Bench Triceps Dip",
        "body_area": ["triceps", "shoulders"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "intermediate",
        "position": "seated",
        "equipment": ["bench"],
        "movement_type": "push",
        "sets": 3,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Place your hands behind you on a sturdy bench with legs extended.",
            "Keep your back close to the bench.",
            "Bend your elbows to lower your body smoothly.",
            "Press back up until your arms are straight."
        ],
        "easier_variation": "Chair Triceps Dip",
        "harder_variation": None
    },

    {
        "id": 70,
        "name": "Close-grip Push-up",
        "body_area": ["triceps", "chest"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "push",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Start in a high plank with hands placed directly under your shoulders.",
            "Keep your elbows tucked close to your ribs as you lower.",
            "Lower your chest toward the floor.",
            "Push back up to the starting position."
        ],
        "easier_variation": "Knee Push-up",
        "harder_variation": "Diamond Push-up"
    },

    {
        "id": 71,
        "name": "Resistance Band Triceps Pushdown",
        "body_area": ["triceps"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["resistance_band"],
        "movement_type": "push",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Anchor a resistance band overhead and hold both ends.",
            "Tuck your elbows close to your sides.",
            "Press your hands downward until your arms are straight.",
            "Return slowly to the starting position."
        ],
        "easier_variation": None,
        "harder_variation": "Chair Triceps Dip"
    },

    {
        "id": 72,
        "name": "Zottman Curl",
        "body_area": ["biceps", "forearms"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "intermediate",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand holding dumbbells with palms facing forward.",
            "Curl the weights up toward your shoulders.",
            "At the top, rotate your wrists so palms face downward.",
            "Lower the dumbbells slowly in that position."
        ],
        "easier_variation": "Biceps Curl",
        "harder_variation": None
    },

    {
        "id": 73,
        "name": "Wrist Curl",
        "body_area": ["forearms"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["dumbbells"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Sit on a chair with your forearms resting on your thighs and palms up.",
            "Hold a light dumbbell in each hand.",
            "Curl your wrists upward comfortably.",
            "Lower the weights slowly."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 74,
        "name": "Reverse Wrist Curl",
        "body_area": ["forearms"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["dumbbells"],
        "movement_type": "raise",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Sit with your forearms resting on your thighs and palms facing down.",
            "Hold a light dumbbell in each hand.",
            "Lift the backs of your hands upward.",
            "Lower slowly back to the start."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 75,
        "name": "Diamond Push-up",
        "body_area": ["triceps", "chest"],
        "goals": ["upper_body_strength"],
        "type": "strength",
        "level": "advanced",
        "position": "floor",
        "equipment": [],
        "movement_type": "push",
        "sets": 3,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Start in a high plank with thumbs and index fingers touching under your chest.",
            "Keep your body in a straight line.",
            "Bend your elbows to lower your chest toward your hands.",
            "Push back up powerfully."
        ],
        "easier_variation": "Close-grip Push-up",
        "harder_variation": None
    },

    # ======================================
    # LOWER BODY (ADDITIONAL: ID 76 - 90)
    # ======================================

    {
        "id": 76,
        "name": "Goblet Squat",
        "body_area": ["quads", "glutes", "core"],
        "goals": ["lower_body_strength", "overall_fitness"],
        "type": "strength",
        "level": "intermediate",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "squat",
        "sets": 3,
        "reps": 10,
        "hold_seconds": None,
        "duration": 5,
        "instructions": [
            "Stand with feet slightly wider than shoulder-width holding one dumbbell at your chest.",
            "Keep your chest upright and core braced.",
            "Bend your knees and hips to lower into a squat.",
            "Push through your feet to stand back up."
        ],
        "easier_variation": "Bodyweight Squat",
        "harder_variation": None
    },

    {
        "id": 77,
        "name": "Sumo Squat",
        "body_area": ["quads", "glutes", "inner_thighs"],
        "goals": ["lower_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "squat",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand with your feet wide and toes pointed slightly outward.",
            "Keep your torso upright as you bend your knees.",
            "Lower your hips comfortably.",
            "Press through your heels to return to standing."
        ],
        "easier_variation": "Chair Squat",
        "harder_variation": "Goblet Squat"
    },

    {
        "id": 78,
        "name": "Wall Sit",
        "body_area": ["quads", "glutes"],
        "goals": ["lower_body_strength", "core_stability"],
        "type": "stability",
        "level": "beginner",
        "position": "standing",
        "equipment": ["wall"],
        "movement_type": "hold",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 3,
        "instructions": [
            "Stand with your back flat against a wall.",
            "Walk your feet forward and slide down until your knees are bent comfortably.",
            "Keep your knees aligned above your ankles.",
            "Hold the position while breathing steadily."
        ],
        "easier_variation": "Chair Squat",
        "harder_variation": None
    },

    {
        "id": 79,
        "name": "Forward Lunge",
        "body_area": ["quads", "glutes"],
        "goals": ["lower_body_strength", "balance"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "lunge",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand tall with your feet hip-width apart.",
            "Step one foot forward and lower your hips until both knees bend.",
            "Keep your front knee aligned over your foot.",
            "Push back to the starting position and switch legs."
        ],
        "easier_variation": "Reverse Lunge",
        "harder_variation": None
    },

    {
        "id": 80,
        "name": "Side Lunge",
        "body_area": ["quads", "glutes", "inner_thighs"],
        "goals": ["lower_body_strength", "mobility"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "lunge",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand upright with your feet together.",
            "Take a wide step out to one side.",
            "Bend the stepping knee and push your hips back while keeping the other leg straight.",
            "Push back to the center and switch sides."
        ],
        "easier_variation": "Sumo Squat",
        "harder_variation": None
    },

    {
        "id": 81,
        "name": "Step-up",
        "body_area": ["quads", "glutes"],
        "goals": ["lower_body_strength", "balance"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["step"],
        "movement_type": "step",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand facing a sturdy low step or platform.",
            "Place one foot completely on the step.",
            "Press through that foot to lift your body up.",
            "Step down slowly and repeat on the other leg."
        ],
        "easier_variation": None,
        "harder_variation": "Split Squat"
    },

    {
        "id": 82,
        "name": "Single-leg Glute Bridge",
        "body_area": ["glutes", "hamstrings", "core"],
        "goals": ["lower_body_strength", "hip_stability"],
        "type": "strength",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "hinge",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Lie on your back with knees bent and feet flat.",
            "Extend one leg straight out.",
            "Press through your planted heel to lift your hips.",
            "Lower slowly and switch sides after completing your reps."
        ],
        "easier_variation": "Glute Bridge",
        "harder_variation": None
    },

    {
        "id": 83,
        "name": "Dumbbell Romanian Deadlift",
        "body_area": ["hamstrings", "glutes", "back"],
        "goals": ["lower_body_strength", "posture"],
        "type": "strength",
        "level": "intermediate",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "hinge",
        "sets": 3,
        "reps": 10,
        "hold_seconds": None,
        "duration": 5,
        "instructions": [
            "Stand with feet hip-width apart holding dumbbells in front of your thighs.",
            "Keep a slight bend in your knees and your back straight.",
            "Push your hips backward to lower the dumbbells along your legs.",
            "Squeeze your glutes to return to standing."
        ],
        "easier_variation": "Good Morning",
        "harder_variation": None
    },

    {
        "id": 84,
        "name": "Seated Calf Raise",
        "body_area": ["calves"],
        "goals": ["lower_body_strength", "accessibility"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["chair"],
        "movement_type": "raise",
        "sets": 2,
        "reps": 15,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Sit upright on a chair with your feet flat on the floor.",
            "Lift your heels as high as comfortable while keeping toes on the floor.",
            "Pause briefly at the top.",
            "Lower your heels slowly."
        ],
        "easier_variation": None,
        "harder_variation": "Calf Raise"
    },

    {
        "id": 85,
        "name": "Side-lying Leg Lift",
        "body_area": ["hips", "glutes"],
        "goals": ["hip_stability", "lower_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "lying",
        "equipment": [],
        "movement_type": "abduction",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Lie on one side with your legs extended and stacked.",
            "Keep your body in a straight line.",
            "Lift your top leg upward comfortably without tilting your hips.",
            "Lower slowly and switch sides after your set."
        ],
        "easier_variation": "Clamshell",
        "harder_variation": None
    },

    {
        "id": 86,
        "name": "Donkey Kick",
        "body_area": ["glutes"],
        "goals": ["lower_body_strength", "hip_stability"],
        "type": "strength",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "lift",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Start on your hands and knees with a flat back.",
            "Keeping your knee bent at 90 degrees, lift one heel toward the ceiling.",
            "Avoid arching your lower back.",
            "Lower your knee and repeat on the other side."
        ],
        "easier_variation": "Glute Bridge",
        "harder_variation": None
    },

    {
        "id": 87,
        "name": "Fire Hydrant",
        "body_area": ["glutes", "hips"],
        "goals": ["hip_stability", "lower_body_strength"],
        "type": "strength",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "abduction",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Start on your hands and knees with your core engaged.",
            "Keep your knee bent and lift one leg out to the side.",
            "Keep your hips level and steady.",
            "Lower the leg slowly and switch sides after completing your reps."
        ],
        "easier_variation": "Clamshell",
        "harder_variation": None
    },

    {
        "id": 88,
        "name": "Split Squat",
        "body_area": ["quads", "glutes"],
        "goals": ["lower_body_strength", "balance"],
        "type": "strength",
        "level": "intermediate",
        "position": "standing",
        "equipment": [],
        "movement_type": "lunge",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand in a staggered stance with one foot forward and one back.",
            "Lower your back knee straight down toward the floor.",
            "Keep your torso upright and front knee aligned.",
            "Push back up and switch legs after finishing the set."
        ],
        "easier_variation": "Supported Reverse Lunge",
        "harder_variation": None
    },

    {
        "id": 89,
        "name": "Supported Reverse Lunge",
        "body_area": ["quads", "glutes"],
        "goals": ["lower_body_strength", "accessibility"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["chair"],
        "movement_type": "lunge",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand beside a sturdy chair and rest one hand on it for balance.",
            "Step one foot backward and bend both knees gently.",
            "Return to the starting position.",
            "Repeat and switch sides."
        ],
        "easier_variation": "Chair Squat",
        "harder_variation": "Reverse Lunge"
    },

    {
        "id": 90,
        "name": "Standing Hamstring Curl",
        "body_area": ["hamstrings"],
        "goals": ["lower_body_strength", "balance"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["chair"],
        "movement_type": "pull",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand behind a sturdy chair and hold the backrest lightly.",
            "Bend one knee to bring your heel toward your glutes.",
            "Keep your thighs aligned.",
            "Lower your foot slowly and switch legs."
        ],
        "easier_variation": None,
        "harder_variation": "Glute Bridge"
    },

    # ======================================
    # CORE (ADDITIONAL: ID 91 - 105)
    # ======================================

    {
        "id": 91,
        "name": "Side Plank",
        "body_area": ["core", "shoulders"],
        "goals": ["core_stability"],
        "type": "stability",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "hold",
        "sets": 2,
        "reps": None,
        "hold_seconds": 15,
        "duration": 3,
        "instructions": [
            "Lie on one side with your forearm on the floor and elbow under your shoulder.",
            "Stack your feet and lift your hips off the floor.",
            "Keep your body in a straight line.",
            "Hold while breathing steadily, then switch sides."
        ],
        "easier_variation": "Knee Side Plank",
        "harder_variation": None
    },

    {
        "id": 92,
        "name": "Knee Side Plank",
        "body_area": ["core"],
        "goals": ["core_stability"],
        "type": "stability",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "hold",
        "sets": 2,
        "reps": None,
        "hold_seconds": 15,
        "duration": 3,
        "instructions": [
            "Lie on your side with your knees bent and forearm on the floor.",
            "Lift your hips so your body forms a straight line from knees to head.",
            "Engage your side abdominal muscles.",
            "Hold comfortably and repeat on the other side."
        ],
        "easier_variation": None,
        "harder_variation": "Side Plank"
    },

    {
        "id": 93,
        "name": "Bicycle Crunch",
        "body_area": ["core"],
        "goals": ["core_stability", "overall_fitness"],
        "type": "strength",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "rotation",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Lie on your back with knees lifted and hands lightly behind your head.",
            "Bring one knee toward your chest while rotating the opposite elbow toward it.",
            "Extend the other leg smoothly.",
            "Alternate sides in a controlled pedaling motion."
        ],
        "easier_variation": "Dead Bug",
        "harder_variation": None
    },

    {
        "id": 94,
        "name": "Basic Crunch",
        "body_area": ["core"],
        "goals": ["core_stability"],
        "type": "strength",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "lift",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Lie on your back with your knees bent and feet flat on the floor.",
            "Place your hands across your chest or lightly behind your ears.",
            "Curl your shoulders slightly off the floor using your abdominal muscles.",
            "Lower back down slowly."
        ],
        "easier_variation": "Seated Knee Lift",
        "harder_variation": "Bicycle Crunch"
    },

    {
        "id": 95,
        "name": "Reverse Crunch",
        "body_area": ["core"],
        "goals": ["core_stability"],
        "type": "strength",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "lift",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Lie on your back with knees bent and feet off the floor.",
            "Place your arms at your sides for support.",
            "Draw your knees toward your chest while lifting your hips slightly.",
            "Lower your hips back down with control."
        ],
        "easier_variation": "Dead Bug",
        "harder_variation": "Leg Raise"
    },

    {
        "id": 96,
        "name": "Russian Twist",
        "body_area": ["core"],
        "goals": ["core_stability"],
        "type": "strength",
        "level": "intermediate",
        "position": "seated",
        "equipment": [],
        "movement_type": "rotation",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Sit on the floor with knees bent and heels resting on the ground.",
            "Lean back slightly while keeping your spine straight.",
            "Rotate your torso gently from one side to the other.",
            "Move with control and breathe steadily."
        ],
        "easier_variation": "Seated Russian Twist",
        "harder_variation": None
    },

    {
        "id": 97,
        "name": "Seated Russian Twist",
        "body_area": ["core"],
        "goals": ["core_stability", "accessibility"],
        "type": "strength",
        "level": "beginner",
        "position": "seated",
        "equipment": ["chair"],
        "movement_type": "rotation",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Sit upright on a sturdy chair with feet flat on the floor.",
            "Clasp your hands together in front of your chest.",
            "Gently rotate your upper body to one side.",
            "Return to the center and rotate to the other side."
        ],
        "easier_variation": None,
        "harder_variation": "Russian Twist"
    },

    {
        "id": 98,
        "name": "Heel Tap",
        "body_area": ["core"],
        "goals": ["core_stability"],
        "type": "strength",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "rotation",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Lie on your back with knees bent and feet flat on the floor.",
            "Lift your head and shoulders slightly off the floor.",
            "Reach one hand toward your same-side heel.",
            "Return to the center and reach toward the opposite heel."
        ],
        "easier_variation": None,
        "harder_variation": "Bicycle Crunch"
    },

    {
        "id": 99,
        "name": "Hollow Body Hold",
        "body_area": ["core"],
        "goals": ["core_stability"],
        "type": "stability",
        "level": "advanced",
        "position": "floor",
        "equipment": [],
        "movement_type": "hold",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 3,
        "instructions": [
            "Lie flat on your back with arms extended overhead and legs straight.",
            "Press your lower back firmly into the floor.",
            "Lift your shoulders and legs slightly off the ground.",
            "Hold the curved position while breathing steadily."
        ],
        "easier_variation": "Dead Bug",
        "harder_variation": None
    },

    {
        "id": 100,
        "name": "Leg Raise",
        "body_area": ["core", "hip_flexors"],
        "goals": ["core_stability"],
        "type": "strength",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "lift",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Lie flat on your back with legs straight and hands at your sides.",
            "Keep your lower back pressed toward the floor.",
            "Lift both legs upward until vertical.",
            "Lower them slowly without letting your lower back arch."
        ],
        "easier_variation": "Bent-knee Leg Raise",
        "harder_variation": None
    },

    {
        "id": 101,
        "name": "Bent-knee Leg Raise",
        "body_area": ["core", "hip_flexors"],
        "goals": ["core_stability"],
        "type": "strength",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "lift",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Lie on your back with your knees bent at 90 degrees.",
            "Engage your core to keep your lower back steady.",
            "Lower your toes gently toward the floor.",
            "Lift your knees back to the starting position."
        ],
        "easier_variation": "Dead Bug",
        "harder_variation": "Leg Raise"
    },

    {
        "id": 102,
        "name": "Plank Shoulder Tap",
        "body_area": ["core", "shoulders"],
        "goals": ["core_stability", "balance"],
        "type": "stability",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "stability",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Start in a high plank position with your feet slightly wider than hip-width.",
            "Keep your hips as still as possible.",
            "Lift one hand to tap your opposite shoulder.",
            "Place your hand down and repeat on the other side."
        ],
        "easier_variation": "Plank",
        "harder_variation": None
    },

    {
        "id": 103,
        "name": "Bear Crawl Hold",
        "body_area": ["core", "shoulders", "quads"],
        "goals": ["core_stability", "overall_fitness"],
        "type": "stability",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "hold",
        "sets": 2,
        "reps": None,
        "hold_seconds": 15,
        "duration": 3,
        "instructions": [
            "Start on your hands and knees with toes tucked under.",
            "Keep your back flat and core braced.",
            "Lift your knees one to two inches off the floor.",
            "Hold the hover position while breathing normally."
        ],
        "easier_variation": "Bird Dog",
        "harder_variation": None
    },

    {
        "id": 104,
        "name": "Standing Side Bend",
        "body_area": ["core"],
        "goals": ["core_stability"],
        "type": "strength",
        "level": "beginner",
        "position": "standing",
        "equipment": ["dumbbells"],
        "movement_type": "rotation",
        "sets": 2,
        "reps": 12,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand tall with feet hip-width apart holding a dumbbell in one hand.",
            "Keep your chest lifted and core engaged.",
            "Bend sideways toward the weighted hand comfortably.",
            "Return upright and switch sides after completing your reps."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 105,
        "name": "Pallof Press",
        "body_area": ["core"],
        "goals": ["core_stability", "posture"],
        "type": "stability",
        "level": "beginner",
        "position": "standing",
        "equipment": ["resistance_band"],
        "movement_type": "stability",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Anchor a resistance band at chest height and stand sideways to it.",
            "Hold the band with both hands against the center of your chest.",
            "Press your hands straight forward without letting your torso twist.",
            "Return your hands to your chest and switch sides after your set."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    # ======================================
    # CARDIO (ADDITIONAL: ID 106 - 120)
    # ======================================

    {
        "id": 106,
        "name": "Jumping Jack",
        "body_area": ["full_body", "legs"],
        "goals": ["cardio", "overall_fitness"],
        "type": "cardio",
        "level": "intermediate",
        "position": "standing",
        "equipment": [],
        "movement_type": "cardio",
        "sets": 2,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand upright with your feet together and arms at your sides.",
            "Jump your feet out wide while swinging your arms overhead.",
            "Jump your feet back together while lowering your arms.",
            "Maintain a steady, comfortable rhythm."
        ],
        "easier_variation": "Low-impact Jumping Jack",
        "harder_variation": None
    },

    {
        "id": 107,
        "name": "High Knees",
        "body_area": ["legs", "core", "full_body"],
        "goals": ["cardio", "overall_fitness"],
        "type": "cardio",
        "level": "intermediate",
        "position": "standing",
        "equipment": [],
        "movement_type": "march",
        "sets": 2,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand upright with your feet hip-width apart.",
            "Drive one knee up toward hip height quickly.",
            "Switch legs rapidly while pumping your arms.",
            "Stay light on the balls of your feet."
        ],
        "easier_variation": "Marching in Place",
        "harder_variation": None
    },

    {
        "id": 108,
        "name": "Butt Kicks",
        "body_area": ["legs", "hamstrings"],
        "goals": ["cardio", "warm_up"],
        "type": "cardio",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "cardio",
        "sets": 2,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand tall with feet hip-width apart.",
            "Jog or step in place while kicking one heel toward your glutes.",
            "Alternate legs smoothly.",
            "Swing your arms naturally at your sides."
        ],
        "easier_variation": "Marching in Place",
        "harder_variation": None
    },

    {
        "id": 109,
        "name": "Mountain Climber",
        "body_area": ["core", "shoulders", "full_body"],
        "goals": ["cardio", "core_stability"],
        "type": "cardio",
        "level": "intermediate",
        "position": "floor",
        "equipment": [],
        "movement_type": "cardio",
        "sets": 2,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Start in a high plank position with hands under your shoulders.",
            "Drive one knee toward your chest.",
            "Switch legs quickly while keeping your hips level.",
            "Continue at a controlled, brisk pace."
        ],
        "easier_variation": "Elevated Mountain Climber",
        "harder_variation": None
    },

    {
        "id": 110,
        "name": "Elevated Mountain Climber",
        "body_area": ["core", "shoulders", "legs"],
        "goals": ["cardio", "core_stability"],
        "type": "cardio",
        "level": "beginner",
        "position": "standing",
        "equipment": ["bench"],
        "movement_type": "cardio",
        "sets": 2,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Place your hands on a sturdy bench in an incline plank position.",
            "Keep your body in a straight line.",
            "Bring one knee forward toward the bench.",
            "Return your foot and alternate legs at a steady pace."
        ],
        "easier_variation": "Marching in Place",
        "harder_variation": "Mountain Climber"
    },

    {
        "id": 111,
        "name": "Shadow Boxing",
        "body_area": ["shoulders", "core", "full_body"],
        "goals": ["cardio", "coordination"],
        "type": "cardio",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "cardio",
        "sets": 2,
        "reps": None,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand in a comfortable staggered stance with hands raised near your chin.",
            "Extend one arm forward in a controlled straight punch.",
            "Return your hand to guard position and punch with the other arm.",
            "Keep your knees soft and core engaged throughout."
        ],
        "easier_variation": "Seated Shadow Boxing",
        "harder_variation": None
    },

    {
        "id": 112,
        "name": "Seated Shadow Boxing",
        "body_area": ["shoulders", "core"],
        "goals": ["cardio", "accessibility"],
        "type": "cardio",
        "level": "beginner",
        "position": "seated",
        "equipment": ["chair"],
        "movement_type": "cardio",
        "sets": 2,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Sit tall on a stable chair with your feet flat on the floor.",
            "Raise your hands near shoulder height.",
            "Punch forward alternating left and right arms.",
            "Keep a steady, energetic pace."
        ],
        "easier_variation": None,
        "harder_variation": "Shadow Boxing"
    },

    {
        "id": 113,
        "name": "Side Step with Arm Swing",
        "body_area": ["full_body", "legs"],
        "goals": ["cardio", "warm_up"],
        "type": "cardio",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "step",
        "sets": 1,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand with your feet together.",
            "Step to the right and bring your left foot to meet it while swinging your arms.",
            "Step to the left and bring your right foot to meet it.",
            "Continue smoothly from side to side."
        ],
        "easier_variation": "Step Touch",
        "harder_variation": None
    },

    {
        "id": 114,
        "name": "Grapevine Step",
        "body_area": ["legs", "full_body"],
        "goals": ["cardio", "coordination"],
        "type": "cardio",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "step",
        "sets": 1,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Step your right foot out to the side.",
            "Cross your left foot behind your right foot.",
            "Step your right foot out again and tap your left foot beside it.",
            "Reverse the pattern moving to the left."
        ],
        "easier_variation": "Step Touch",
        "harder_variation": None
    },

    {
        "id": 115,
        "name": "Basic Burpee",
        "body_area": ["full_body"],
        "goals": ["cardio", "overall_fitness"],
        "type": "cardio",
        "level": "advanced",
        "position": "standing",
        "equipment": [],
        "movement_type": "cardio",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand with feet shoulder-width apart.",
            "Squat down and place your hands on the floor.",
            "Jump your feet back into a plank, then jump them forward toward your hands.",
            "Stand up or add a small jump with arms overhead."
        ],
        "easier_variation": "Step-back Burpee",
        "harder_variation": None
    },

    {
        "id": 116,
        "name": "Step-back Burpee",
        "body_area": ["full_body"],
        "goals": ["cardio", "overall_fitness"],
        "type": "cardio",
        "level": "intermediate",
        "position": "standing",
        "equipment": [],
        "movement_type": "cardio",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Squat down and place both hands firmly on the floor.",
            "Step one foot back at a time into a high plank.",
            "Step your feet forward one at a time toward your hands.",
            "Stand up tall and reach your arms overhead."
        ],
        "easier_variation": "Low-impact Jumping Jack",
        "harder_variation": "Basic Burpee"
    },

    {
        "id": 117,
        "name": "Skater Step",
        "body_area": ["legs", "glutes", "full_body"],
        "goals": ["cardio", "balance"],
        "type": "cardio",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "step",
        "sets": 2,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Step widely to your right and sweep your left foot behind your right ankle.",
            "Swing your arms across your body naturally.",
            "Step widely to your left and sweep your right foot behind.",
            "Continue alternating sides at a comfortable pace."
        ],
        "easier_variation": "Step Touch",
        "harder_variation": "Speed Skater"
    },

    {
        "id": 118,
        "name": "Speed Skater",
        "body_area": ["legs", "glutes", "full_body"],
        "goals": ["cardio", "coordination"],
        "type": "cardio",
        "level": "intermediate",
        "position": "standing",
        "equipment": [],
        "movement_type": "cardio",
        "sets": 2,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Leap sideways onto your right foot while bringing your left foot behind you.",
            "Bend your landing knee slightly to absorb the movement.",
            "Bound sideways onto your left foot.",
            "Continue hopping side-to-side smoothly."
        ],
        "easier_variation": "Skater Step",
        "harder_variation": None
    },

    {
        "id": 119,
        "name": "Alternating Front Kick",
        "body_area": ["legs", "core"],
        "goals": ["cardio", "coordination"],
        "type": "cardio",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "cardio",
        "sets": 2,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand upright with your core braced and hands near your waist.",
            "Lift one knee and extend your foot forward in a controlled kick.",
            "Lower your foot back to the floor.",
            "Repeat with the opposite leg at a steady rhythm."
        ],
        "easier_variation": "Marching in Place",
        "harder_variation": None
    },

    {
        "id": 120,
        "name": "Invisible Jump Rope",
        "body_area": ["calves", "shoulders", "full_body"],
        "goals": ["cardio", "coordination"],
        "type": "cardio",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "cardio",
        "sets": 2,
        "reps": None,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand with feet together and elbows close to your sides.",
            "Rotate your wrists as if turning a jump rope.",
            "Perform small, light hops or alternate heel lifts.",
            "Keep a steady, comfortable pace."
        ],
        "easier_variation": "Marching in Place",
        "harder_variation": "Jumping Jack"
    },

    # ======================================
    # BALANCE (ADDITIONAL: ID 121 - 135)
    # ======================================

    {
        "id": 121,
        "name": "Single-leg Balance",
        "body_area": ["legs", "core"],
        "goals": ["balance", "coordination"],
        "type": "balance",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "balance",
        "sets": 2,
        "reps": None,
        "hold_seconds": 15,
        "duration": 2,
        "instructions": [
            "Stand upright with your feet together near a wall or chair if needed.",
            "Shift your weight onto one foot and lift the other foot off the floor.",
            "Focus your gaze on a steady point ahead.",
            "Lower your foot and switch sides."
        ],
        "easier_variation": "Supported Single-leg Balance",
        "harder_variation": "Single-leg Reach"
    },

    {
        "id": 122,
        "name": "Heel-to-Toe Walk",
        "body_area": ["legs", "core"],
        "goals": ["balance", "coordination"],
        "type": "balance",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "balance",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand upright looking forward.",
            "Step one foot directly in front of the other so the heel touches the toes.",
            "Move slowly in a straight line.",
            "Turn around carefully and walk back."
        ],
        "easier_variation": "Tandem Stance",
        "harder_variation": None
    },

    {
        "id": 123,
        "name": "Single-leg Reach",
        "body_area": ["legs", "core", "glutes"],
        "goals": ["balance", "hip_stability"],
        "type": "balance",
        "level": "intermediate",
        "position": "standing",
        "equipment": [],
        "movement_type": "balance",
        "sets": 2,
        "reps": 6,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand on one leg with a slight bend in your supporting knee.",
            "Hinge forward slightly at the hips while extending your free leg behind you.",
            "Reach one hand toward your shin comfortably.",
            "Return to upright and switch legs after completing your reps."
        ],
        "easier_variation": "Single-leg Balance",
        "harder_variation": None
    },

    {
        "id": 124,
        "name": "Clock Reach",
        "body_area": ["legs", "core", "hips"],
        "goals": ["balance", "coordination"],
        "type": "balance",
        "level": "intermediate",
        "position": "standing",
        "equipment": [],
        "movement_type": "balance",
        "sets": 2,
        "reps": 6,
        "hold_seconds": None,
        "duration": 4,
        "instructions": [
            "Stand on one leg imagining you are in the center of a clock.",
            "Tap your free foot lightly toward 12 o'clock, 3 o'clock, and 6 o'clock.",
            "Keep your supporting knee steady and torso upright.",
            "Switch legs and repeat in the opposite direction."
        ],
        "easier_variation": "Single-leg Balance",
        "harder_variation": None
    },

    {
        "id": 125,
        "name": "Standing Tree Pose",
        "body_area": ["legs", "core", "hips"],
        "goals": ["balance", "hip_stability"],
        "type": "balance",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "balance",
        "sets": 2,
        "reps": None,
        "hold_seconds": 15,
        "duration": 3,
        "instructions": [
            "Stand tall and shift your weight onto your left foot.",
            "Place the sole of your right foot against your left ankle or calf.",
            "Bring your hands together at your chest.",
            "Hold steadily while breathing, then switch sides."
        ],
        "easier_variation": "Supported Tree Pose",
        "harder_variation": None
    },

    {
        "id": 126,
        "name": "Supported Tree Pose",
        "body_area": ["legs", "core", "hips"],
        "goals": ["balance", "accessibility"],
        "type": "balance",
        "level": "beginner",
        "position": "standing",
        "equipment": ["wall"],
        "movement_type": "balance",
        "sets": 2,
        "reps": None,
        "hold_seconds": 15,
        "duration": 3,
        "instructions": [
            "Stand beside a wall with one hand resting lightly on it.",
            "Place the sole of your outer foot against your inner ankle or calf.",
            "Keep your posture tall and hips level.",
            "Hold comfortably and switch sides."
        ],
        "easier_variation": None,
        "harder_variation": "Standing Tree Pose"
    },

    {
        "id": 127,
        "name": "Weight Shift Side-to-Side",
        "body_area": ["legs", "core"],
        "goals": ["balance", "accessibility"],
        "type": "balance",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "balance",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 2,
        "instructions": [
            "Stand with your feet hip-width apart.",
            "Slowly shift your weight onto your right foot and lift your left heel.",
            "Pause briefly, then shift your weight onto your left foot.",
            "Continue moving slowly with control."
        ],
        "easier_variation": None,
        "harder_variation": "Single-leg Balance"
    },

    {
        "id": 128,
        "name": "Front-to-Back Weight Shift",
        "body_area": ["legs", "calves", "core"],
        "goals": ["balance", "accessibility"],
        "type": "balance",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "balance",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 2,
        "instructions": [
            "Stand with your feet hip-width apart near a counter or wall.",
            "Lean gently forward from your ankles so weight moves toward your toes.",
            "Shift smoothly backward so weight moves toward your heels.",
            "Keep your body straight without bending at the waist."
        ],
        "easier_variation": None,
        "harder_variation": "Tandem Stance"
    },

    {
        "id": 129,
        "name": "Single-leg Calf Raise Hold",
        "body_area": ["calves", "legs", "core"],
        "goals": ["balance", "lower_body_strength"],
        "type": "balance",
        "level": "intermediate",
        "position": "standing",
        "equipment": [],
        "movement_type": "balance",
        "sets": 2,
        "reps": None,
        "hold_seconds": 10,
        "duration": 3,
        "instructions": [
            "Stand on one foot near a wall for light support if needed.",
            "Press onto the ball of your standing foot to lift your heel.",
            "Hold the raised position steadily.",
            "Lower your heel slowly and switch legs."
        ],
        "easier_variation": "Calf Raise",
        "harder_variation": None
    },

    {
        "id": 130,
        "name": "March with Pause",
        "body_area": ["legs", "core", "hip_flexors"],
        "goals": ["balance", "coordination"],
        "type": "balance",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "balance",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand tall with your feet hip-width apart.",
            "Lift one knee to hip height and pause for two seconds.",
            "Place your foot down with control.",
            "Lift the opposite knee and pause."
        ],
        "easier_variation": "Supported March with Pause",
        "harder_variation": None
    },

    {
        "id": 131,
        "name": "Supported March with Pause",
        "body_area": ["legs", "core", "hip_flexors"],
        "goals": ["balance", "accessibility"],
        "type": "balance",
        "level": "beginner",
        "position": "standing",
        "equipment": ["chair"],
        "movement_type": "balance",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand behind a sturdy chair with hands resting lightly on the backrest.",
            "Lift one knee comfortably and hold for two seconds.",
            "Lower your foot slowly.",
            "Repeat with the other leg."
        ],
        "easier_variation": None,
        "harder_variation": "March with Pause"
    },

    {
        "id": 132,
        "name": "Single-leg Ball Pass",
        "body_area": ["legs", "core", "shoulders"],
        "goals": ["balance", "coordination"],
        "type": "balance",
        "level": "intermediate",
        "position": "standing",
        "equipment": ["ball"],
        "movement_type": "balance",
        "sets": 2,
        "reps": 8,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand on one leg while holding a light ball in front of you.",
            "Pass the ball slowly from one hand to the other around your waist.",
            "Keep your posture tall and standing leg steady.",
            "Switch legs and repeat."
        ],
        "easier_variation": "Single-leg Balance",
        "harder_variation": None
    },

    {
        "id": 133,
        "name": "Standing Hip Abduction Hold",
        "body_area": ["hips", "glutes", "core"],
        "goals": ["balance", "hip_stability"],
        "type": "balance",
        "level": "beginner",
        "position": "standing",
        "equipment": ["chair"],
        "movement_type": "balance",
        "sets": 2,
        "reps": None,
        "hold_seconds": 10,
        "duration": 3,
        "instructions": [
            "Stand behind a sturdy chair holding the backrest lightly.",
            "Lift one straight leg out to the side a few inches.",
            "Keep your torso upright without leaning.",
            "Hold steadily, lower your leg, and switch sides."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 134,
        "name": "Eyes-closed Tandem Stance",
        "body_area": ["legs", "core"],
        "goals": ["balance", "coordination"],
        "type": "balance",
        "level": "intermediate",
        "position": "standing",
        "equipment": [],
        "movement_type": "balance",
        "sets": 2,
        "reps": None,
        "hold_seconds": 15,
        "duration": 2,
        "instructions": [
            "Stand next to a sturdy wall or counter for safety.",
            "Place one foot directly in front of the other heel-to-toe.",
            "Close your eyes gently and maintain your balance.",
            "Open your eyes, switch feet, and repeat."
        ],
        "easier_variation": "Tandem Stance",
        "harder_variation": None
    },

    {
        "id": 135,
        "name": "Tightrope Side Step",
        "body_area": ["legs", "core"],
        "goals": ["balance", "coordination"],
        "type": "balance",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "balance",
        "sets": 2,
        "reps": 10,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Stand tall with your arms out to your sides for balance.",
            "Step slowly to the right, crossing your left foot neatly in front of your right.",
            "Step your right foot out to the side again.",
            "Move slowly and repeat in the opposite direction."
        ],
        "easier_variation": "Step Touch",
        "harder_variation": None
    },

    # ======================================
    # MOBILITY AND FLEXIBILITY (ADDITIONAL: ID 136 - 150)
    # ======================================

    {
        "id": 136,
        "name": "Neck Tilt Stretch",
        "body_area": ["neck", "shoulders"],
        "goals": ["mobility", "cool_down"],
        "type": "flexibility",
        "level": "beginner",
        "position": "seated",
        "equipment": [],
        "movement_type": "stretch",
        "sets": 2,
        "reps": None,
        "hold_seconds": 15,
        "duration": 2,
        "instructions": [
            "Sit upright with your shoulders relaxed and down.",
            "Gently tilt your right ear toward your right shoulder.",
            "Hold the mild stretch comfortably without forcing.",
            "Return to center and repeat on the left side."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 137,
        "name": "Neck Rotation",
        "body_area": ["neck"],
        "goals": ["mobility", "warm_up"],
        "type": "mobility",
        "level": "beginner",
        "position": "seated",
        "equipment": [],
        "movement_type": "mobility",
        "sets": 1,
        "reps": 8,
        "hold_seconds": None,
        "duration": 2,
        "instructions": [
            "Sit tall looking straight ahead.",
            "Slowly turn your head to look over your right shoulder.",
            "Return smoothly to the center.",
            "Turn slowly to look over your left shoulder."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 138,
        "name": "Shoulder Roll",
        "body_area": ["shoulders", "back"],
        "goals": ["mobility", "warm_up"],
        "type": "mobility",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "mobility",
        "sets": 1,
        "reps": 10,
        "hold_seconds": None,
        "duration": 2,
        "instructions": [
            "Stand comfortably with your arms relaxed at your sides.",
            "Lift your shoulders up toward your ears, roll them back, and press them down.",
            "Complete smooth circular motions.",
            "Reverse the direction halfway through."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 139,
        "name": "Overhead Triceps Stretch",
        "body_area": ["triceps", "shoulders"],
        "goals": ["mobility", "cool_down"],
        "type": "flexibility",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "stretch",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 2,
        "instructions": [
            "Raise one arm overhead and bend your elbow so your hand reaches toward your upper back.",
            "Use your opposite hand to gently support the raised elbow.",
            "Hold the stretch comfortably while standing tall.",
            "Release and switch arms."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 140,
        "name": "Doorway Chest Stretch",
        "body_area": ["chest", "shoulders"],
        "goals": ["mobility", "posture", "cool_down"],
        "type": "flexibility",
        "level": "beginner",
        "position": "standing",
        "equipment": ["wall"],
        "movement_type": "stretch",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 2,
        "instructions": [
            "Stand in an open doorway or beside a wall with your forearm resting against it.",
            "Keep your elbow bent at shoulder height.",
            "Step forward slightly until you feel a gentle stretch across your chest.",
            "Hold comfortably and switch sides."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 141,
        "name": "Seated Spinal Twist",
        "body_area": ["back", "core"],
        "goals": ["mobility", "cool_down"],
        "type": "flexibility",
        "level": "beginner",
        "position": "seated",
        "equipment": ["chair"],
        "movement_type": "stretch",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 3,
        "instructions": [
            "Sit tall on a chair with your feet flat on the floor.",
            "Place your right hand on the outside of your left thigh.",
            "Gently twist your upper body to the left while keeping your spine long.",
            "Hold while breathing deeply, then switch sides."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 142,
        "name": "Child's Pose",
        "body_area": ["back", "shoulders", "hips"],
        "goals": ["mobility", "cool_down"],
        "type": "flexibility",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "stretch",
        "sets": 2,
        "reps": None,
        "hold_seconds": 25,
        "duration": 3,
        "instructions": [
            "Kneel on the floor and sit your hips back toward your heels.",
            "Walk your hands forward on the floor and lower your chest gently.",
            "Rest your forehead comfortably toward the mat.",
            "Hold and take slow, deep breaths."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 143,
        "name": "Seated Hamstring Stretch",
        "body_area": ["hamstrings", "back"],
        "goals": ["mobility", "cool_down"],
        "type": "flexibility",
        "level": "beginner",
        "position": "seated",
        "equipment": [],
        "movement_type": "stretch",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 3,
        "instructions": [
            "Sit on the floor with one leg extended straight and the other foot against your inner thigh.",
            "Sit tall and hinge forward slightly from your hips.",
            "Reach toward your shin or ankle comfortably.",
            "Hold the stretch and switch legs."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 144,
        "name": "Standing Quad Stretch",
        "body_area": ["quads", "hip_flexors"],
        "goals": ["mobility", "cool_down"],
        "type": "flexibility",
        "level": "beginner",
        "position": "standing",
        "equipment": ["chair"],
        "movement_type": "stretch",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 3,
        "instructions": [
            "Stand beside a sturdy chair and hold it with one hand for balance.",
            "Bend your opposite knee and hold your ankle behind you.",
            "Keep your knees close together and torso upright.",
            "Hold gently and switch legs."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 145,
        "name": "Kneeling Hip Flexor Stretch",
        "body_area": ["hip_flexors", "quads"],
        "goals": ["mobility", "cool_down"],
        "type": "flexibility",
        "level": "beginner",
        "position": "floor",
        "equipment": [],
        "movement_type": "stretch",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 3,
        "instructions": [
            "Kneel on one knee with your other foot planted flat in front of you.",
            "Keep your torso upright and gently shift your hips forward.",
            "Feel a mild stretch in the front of your back hip.",
            "Hold comfortably and switch sides."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 146,
        "name": "Figure-four Glute Stretch",
        "body_area": ["glutes", "hips"],
        "goals": ["mobility", "cool_down"],
        "type": "flexibility",
        "level": "beginner",
        "position": "lying",
        "equipment": [],
        "movement_type": "stretch",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 3,
        "instructions": [
            "Lie on your back with knees bent and feet flat on the floor.",
            "Cross one ankle over your opposite knee.",
            "Gently draw your uncrossed thigh toward your chest if comfortable.",
            "Hold the stretch and switch legs."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 147,
        "name": "Butterfly Stretch",
        "body_area": ["inner_thighs", "hips"],
        "goals": ["mobility", "cool_down"],
        "type": "flexibility",
        "level": "beginner",
        "position": "seated",
        "equipment": [],
        "movement_type": "stretch",
        "sets": 2,
        "reps": None,
        "hold_seconds": 20,
        "duration": 3,
        "instructions": [
            "Sit on the floor and bring the soles of your feet together.",
            "Allow your knees to relax outward toward the floor.",
            "Hold your ankles and sit tall.",
            "Hold comfortably while breathing steadily."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 148,
        "name": "Hip Circles",
        "body_area": ["hips", "back"],
        "goals": ["mobility", "warm_up"],
        "type": "mobility",
        "level": "beginner",
        "position": "standing",
        "equipment": [],
        "movement_type": "mobility",
        "sets": 1,
        "reps": 8,
        "hold_seconds": None,
        "duration": 2,
        "instructions": [
            "Stand with feet shoulder-width apart and hands on your hips.",
            "Move your hips in a wide, smooth circle.",
            "Keep your upper body relaxed.",
            "Switch directions after completing your reps."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 149,
        "name": "Ankle Circles",
        "body_area": ["calves", "legs"],
        "goals": ["mobility", "warm_up"],
        "type": "mobility",
        "level": "beginner",
        "position": "seated",
        "equipment": [],
        "movement_type": "mobility",
        "sets": 1,
        "reps": 10,
        "hold_seconds": None,
        "duration": 2,
        "instructions": [
            "Sit comfortably and lift one foot slightly off the floor.",
            "Rotate your ankle slowly in a full circle.",
            "Reverse the circle direction.",
            "Lower your foot and repeat with the other ankle."
        ],
        "easier_variation": None,
        "harder_variation": None
    },

    {
        "id": 150,
        "name": "Thoracic Open Book",
        "body_area": ["back", "chest", "shoulders"],
        "goals": ["mobility", "posture"],
        "type": "mobility",
        "level": "beginner",
        "position": "lying",
        "equipment": [],
        "movement_type": "mobility",
        "sets": 2,
        "reps": 6,
        "hold_seconds": None,
        "duration": 3,
        "instructions": [
            "Lie on one side with your knees bent and arms extended together in front of you.",
            "Keep your knees together on the floor.",
            "Sweep your top arm up and over toward the opposite side like opening a book.",
            "Return smoothly and repeat on the other side."
        ],
        "easier_variation": None,
        "harder_variation": None
    }

]

# Keep a focused set for LockIn. The omitted records remain above so the
# database can be expanded later without having to recreate them.
excluded_exercise_ids = [
    31, 38, 41, 44, 45, 48, 50, 54, 55, 57,
    58, 59, 62, 63, 64, 67, 69, 72, 73, 74,
    75, 77, 84, 87, 90, 97, 103, 104, 112, 113,
    114, 117, 119, 124, 126, 128, 132, 133, 135, 136
]

curated_exercises = []

for exercise in exercises:
    if exercise["id"] not in excluded_exercise_ids:
        curated_exercises.append(exercise)

# Normalize fields used by the recommendation system. Planning values such as
# sets, repetitions, hold time, intervals, and duration are LockIn estimates,
# not values imported from the external dataset.
cardio_intervals = {
    "Jumping Jack": [30, 30],
    "High Knees": [30, 30],
    "Butt Kicks": [30, 30],
    "Mountain Climber": [30, 30],
    "Elevated Mountain Climber": [30, 30],
    "Shadow Boxing": [45, 30],
    "Speed Skater": [30, 30],
    "Invisible Jump Rope": [30, 30]
}

for new_id in range(len(curated_exercises)):
    exercise = curated_exercises[new_id]
    exercise["id"] = new_id + 1
    exercise["exercise_type"] = exercise["type"]
    exercise["work_seconds"] = None
    exercise["rest_seconds"] = None
    exercise["video_url"] = None

    if exercise["name"] in cardio_intervals:
        interval = cardio_intervals[exercise["name"]]
        exercise["work_seconds"] = interval[0]
        exercise["rest_seconds"] = interval[1]

exercise_names = []

for exercise in curated_exercises:
    exercise_names.append(exercise["name"])

for exercise in curated_exercises:
    if exercise["easier_variation"] not in exercise_names:
        exercise["easier_variation"] = None
    if exercise["harder_variation"] not in exercise_names:
        exercise["harder_variation"] = None

exercises = curated_exercises

# DATABASE CHECK

if __name__ == "__main__":

    print("Total exercises:", len(exercises))

    ids = []

    for exercise in exercises:
        ids.append(exercise["id"])

    if len(ids) == len(set(ids)):
        print("ID check: Passed")
    else:
        print("ID check: Duplicate IDs found")

    exercise_types = {}

    for exercise in exercises:

        exercise_type = exercise["type"]

        if exercise_type not in exercise_types:
            exercise_types[exercise_type] = 0

        exercise_types[exercise_type] += 1

    print("\nExercises by type:")

    for exercise_type in exercise_types:
        print(exercise_type, ":", exercise_types[exercise_type])

    required_fields = [
        "id",
        "name",
        "body_area",
        "goals",
        "type",
        "level",
        "position",
        "equipment",
        "movement_type",
        "sets",
        "reps",
        "hold_seconds",
        "duration",
        "instructions"
    ]

    errors = 0

    for exercise in exercises:
        for field in required_fields:
            if field not in exercise:
                print("Missing field:", field, "in", exercise["name"])
                errors += 1

    if errors == 0:
        print("\nField check: Passed")
    else:
        print("\nField check:", errors, "errors")
