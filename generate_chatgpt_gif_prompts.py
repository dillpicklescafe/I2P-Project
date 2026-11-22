"""Generate standalone ChatGPT prompts for LockIn's 24 missing GIFs."""

from __future__ import annotations

from pathlib import Path

from exercises import exercises


OUTPUT_PATH = Path("CHATGPT_GIF_PROMPTS_24.md")
MISSING_IDS = [
    128, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162,
    163, 164, 165, 166, 167, 169, 170, 172, 173, 174, 175, 176,
]


SPECS = {
    128: {
        "start": "Stand upright in side profile, feet hip-width apart and parallel, arms relaxed, knees soft, and the head, ribs, pelvis, and ankles stacked in one straight line. A plain wall or counter is nearby but does not hide the body.",
        "frames": [
            "Neutral upright stance with pressure centered over the whole foot.",
            "The entire straight body begins to incline forward from the ankle joints; heels remain down.",
            "Forward endpoint: pressure is toward the toes, with no bend at the waist and no heel lift.",
            "Return as one straight unit to neutral.",
            "The straight body begins to incline backward from the ankles; toes remain down.",
            "Backward endpoint: pressure is toward the heels, with hips and shoulders still aligned.",
            "Return exactly to the neutral opening pose for a seamless loop.",
        ],
        "camera": "Fixed full-body side view at waist height so the ankle pivot, heels, toes, head, and posture are all visible.",
        "details": "The motion is a small ankle strategy, not a hip hinge. Both feet stay fully planted. Keep the line from ankles through hips to shoulders straight.",
        "avoid": "Do not bend at the waist, squat, step, lift the heels or toes, sway the camera, crop the feet, or turn this into a calf raise.",
        "frames_count": 7,
    },
    152: {
        "support": "Database equipment list: none. The instructions explicitly require one stable, armless chair.",
        "start": "Sit tall in the center of a stable armless chair, facing the camera, feet flat and hip-width apart, knees bent about 90 degrees, pelvis level, and both arms extended sideways at shoulder height.",
        "frames": [
            "Opening chair posture with both feet planted and arms at shoulder height.",
            "Lift the left knee while the right hand travels diagonally toward it for a cross-body knee reach; torso remains tall.",
            "Return the left foot and right arm to the opening posture.",
            "Reach both arms overhead without shrugging or leaning back.",
            "Return both arms to shoulder height.",
            "Tap the left toes laterally to the left while the right foot stays planted and the torso stays centered.",
            "Return the left foot to center.",
            "Lift the right knee while the left hand makes the opposite cross-body knee reach.",
            "Return to the opening posture.",
            "Reach both arms overhead again.",
            "Tap the right toes laterally to the right after lowering the arms, keeping the body on the chair.",
            "Return feet and arms exactly to the opening pose for the loop.",
        ],
        "camera": "Fixed straight-on full-body view, slightly above seated waist height, wide enough to show the chair, both hands overhead, and both lateral toe taps.",
        "details": "Show the ordered flow clearly: cross-body knee reach, overhead reach, lateral toe tap, then repeat with the other side leading. The seated pelvis stays on the chair throughout.",
        "avoid": "Do not omit the chair, lean away from a reach, stand up, cross the legs, turn the toe tap into a kick, add extra movements, or crop hands or feet.",
        "frames_count": 12,
    },
    153: {
        "start": "Stand facing the camera on the right leg with the right knee softly bent, pelvis level, trunk braced and upright, arms slightly out for balance, and the left foot hovering close to center.",
        "frames": [
            "Stable right-leg balance at center.",
            "Reach the hovering left foot forward without transferring weight to it.",
            "Return the left foot to hover at center.",
            "Reach the left foot sideways while the right knee remains softly bent.",
            "Return to center.",
            "Reach the left foot behind while keeping the pelvis square and trunk steady.",
            "Return to center and briefly place both feet down to reset.",
            "Shift into a stable left-leg balance with the right foot hovering.",
            "Reach the right foot forward without touching down if possible, then return to center.",
            "Reach the right foot sideways, then return to center.",
            "Reach the right foot behind, then return to center.",
            "Finish with both feet down in the same neutral orientation as the reset, ready to loop into the right-leg balance.",
        ],
        "camera": "Fixed front three-quarter full-body view so forward, lateral, and backward foot directions remain distinguishable and both feet are always visible.",
        "details": "The reaching foot stays light and preferably hovering. The standing knee remains softly bent; hips stay level and the torso does not collapse or rotate.",
        "avoid": "Do not turn the movement into a lunge, touch substantial weight onto the reaching foot, lock the standing knee, tip the torso excessively, skip either side, or change camera angle.",
        "frames_count": 12,
    },
    154: {
        "start": "Begin in a strong high plank in side profile, palms directly under shoulders, arms straight but not hyperextended, feet about hip-width, neck neutral, and head, shoulders, hips, knees, and heels in one line.",
        "frames": [
            "Opening high plank.",
            "First third of a slow three-second lowering: elbows angle back and the whole body descends together.",
            "Second third of the lowering with chest closer to the floor and hips still aligned.",
            "Bottom of the lowering, chest hovering just above the floor.",
            "Hold the bottom position for the visible one-second pause without touching down.",
            "Begin pressing upward as one rigid unit.",
            "Continue pressing with elbows extending and hips neither sagging nor piking.",
            "Return exactly to the opening high plank for a seamless loop.",
        ],
        "camera": "Fixed full-body side view at low waist height, showing palms, elbow path, chest clearance, hips, knees, and feet.",
        "details": "Make the eccentric lowering visibly slower than the upward press. Preserve a straight plank line and the one-second bottom pause.",
        "avoid": "Do not bounce, touch the chest down, flare elbows sideways, lead with the hips, sag the lower back, raise the hips, move the camera, or perform a normal-speed push-up.",
        "frames_count": 8,
    },
    155: {
        "start": "Face the camera in a stable right-leg balance, right knee softly bent, left foot hovering, arms in a natural counterbalance position, chest lifted, and pelvis level.",
        "frames": [
            "Stable right-leg starting balance.",
            "Send the hips backward and begin a shallow squat on the right leg; left leg remains free.",
            "Reach the shallow single-leg squat endpoint with right knee tracking over the toes.",
            "Drive through the right foot to stand while the left knee travels forward and upward.",
            "Reach the left-knee-drive endpoint with tall posture.",
            "Lower the left foot and reset with both feet briefly stable.",
            "Transfer into left-leg balance.",
            "Perform the same shallow single-leg squat on the left leg.",
            "Stand through the left foot and drive the right knee forward.",
            "Reset to the same two-foot neutral stance so the loop can begin again.",
        ],
        "camera": "Fixed front three-quarter full-body view, wide enough to show the hip shift, standing-knee alignment, both feet, and both knee drives.",
        "details": "Keep each squat shallow and controlled. The standing knee tracks with the toes, the heel stays planted, and balance is visibly reset before changing sides.",
        "avoid": "Do not perform a deep pistol squat, hop, let the knee collapse inward, touch the free foot down during the squat, round the spine, skip one side, or crop the feet.",
        "frames_count": 10,
    },
    156: {
        "start": "Stand tall facing slightly toward the camera, feet hip-width, arms relaxed, and enough clear floor behind for reverse lunges.",
        "frames": [
            "Neutral standing posture.",
            "Step the right foot backward into a comfortable reverse lunge with the left foot forward.",
            "At the lunge depth, rotate the chest toward the left front leg while hips remain stable.",
            "Untwist and step forward toward standing.",
            "Stand tall and sweep both arms overhead.",
            "Lower the arms and step the left foot backward into the opposite reverse lunge.",
            "Rotate the chest toward the right front leg.",
            "Untwist and step forward.",
            "Stand tall and sweep both arms overhead again.",
            "Lower the arms to the exact neutral opening pose for a seamless loop.",
        ],
        "camera": "Fixed front three-quarter full-body view, wide enough for both backward steps and overhead arm sweeps.",
        "details": "Rotate toward the front leg on each side. Keep the front foot grounded, the range pain-free, and every transition continuous without bouncing.",
        "avoid": "Do not rotate away from the front leg, kneel onto the floor, add a jump, pulse or bounce, omit one side, crop overhead hands, or move the camera.",
        "frames_count": 10,
    },
    157: {
        "start": "Stand tall in a front three-quarter orientation with clear floor space and arms relaxed.",
        "frames": [
            "Neutral standing posture.",
            "Step the right foot backward into a reverse lunge, left foot forward.",
            "Rotate the chest toward the left front leg while staying in the lunge.",
            "Untwist and place both hands on the floor beside the left front foot.",
            "Shift the hips backward and straighten the left front leg briefly into a comfortable hamstring position.",
            "Rebend the left knee and return to the lunge with hands controlled.",
            "Lift the hands, step through, and stand tall.",
            "Step the left foot backward into the opposite reverse lunge.",
            "Rotate the chest toward the right front leg.",
            "Untwist and place both hands beside the right front foot.",
            "Shift back and briefly straighten the right front leg.",
            "Rebend the right knee and return to the lunge.",
            "Lift the hands, step through, and stand.",
            "Finish in the exact opening stance for the loop.",
        ],
        "camera": "Fixed wide front three-quarter full-body view, low enough to show hand placement and leg straightening but wide enough to keep the standing posture visible.",
        "details": "Preserve the exact order on each side: reverse lunge, rotate toward front leg, hands down, front leg straightens, return to lunge, step through to stand.",
        "avoid": "Do not omit hand placement, straighten the rear leg instead of the front leg, turn it into a push-up or burpee, bounce in the stretch, rush transitions, omit a side, or crop limbs.",
        "frames_count": 14,
    },
    158: {
        "start": "Begin half-kneeling with the right foot forward, left knee comfortably on the floor, torso tall, pelvis neutral, and arms relaxed.",
        "frames": [
            "Right-side half-kneeling hip-flexor stretch with torso upright.",
            "Shift the hips gently forward within a pain-free range.",
            "Shift the hips backward and begin straightening the right front leg.",
            "Reach a comfortable right half split with the spine long.",
            "Return to half-kneeling.",
            "Raise the left arm and make a gentle side bend toward the right, lengthening the left side body.",
            "Return upright.",
            "Transition carefully to left foot forward and right knee down.",
            "Show the left-side half-kneeling hip-flexor stretch.",
            "Shift back into a comfortable left half split.",
            "Return to half-kneeling.",
            "Raise the right arm and side-bend gently toward the left.",
            "Return upright and transition back toward the original kneeling arrangement.",
            "Recreate the opening right-side half-kneeling pose for the loop.",
        ],
        "camera": "Fixed full-body side/front three-quarter view showing both knee positions, front-leg straightening, spine, and overhead side-bend arm.",
        "details": "Movement is slow and recovery-focused. Keep all joints comfortable, the breath relaxed, and show the complete sequence on both sides.",
        "avoid": "Do not force a deep split, bounce, arch the lower back, collapse onto the front thigh, omit the side bend or either side, change identity, or crop the kneeling leg.",
        "frames_count": 14,
    },
    159: {
        "start": "Begin with the right foot forward in a comfortable half-kneeling hip stretch, left knee supported on the floor, torso tall and neutral.",
        "frames": [
            "Right-side half-kneeling hip stretch; pause as if taking one relaxed breath.",
            "Shift the hips back and begin straightening the right front leg.",
            "Right half split with long spine; pause for one relaxed breath.",
            "Return forward to half-kneeling.",
            "Rotate the rib cage gently toward the right front leg, using a comfortable arm opening; pause for one breath.",
            "Reverse the rotation back to neutral half-kneeling.",
            "Reverse into the half split again, then return to half-kneeling, visibly retracing the sequence.",
            "Change sides carefully so the left foot is forward and right knee is down.",
            "Left-side half-kneeling hip stretch; pause for one breath.",
            "Shift back into a left half split; pause for one breath.",
            "Return to half-kneeling.",
            "Rotate gently toward the left front leg; pause for one breath.",
            "Reverse the rotation to neutral.",
            "Reverse through the left half split and back to half-kneeling.",
            "Transition back to the original right-foot-forward arrangement.",
            "Match the opening pose exactly for a seamless loop.",
        ],
        "camera": "Fixed wide front three-quarter floor-level view showing both legs, the half split, and the direction of trunk rotation on each side.",
        "details": "Each side must include half-kneeling hip stretch, half split, gentle rotation, and a true reversed sequence before switching sides. Pauses should read as calm breaths.",
        "avoid": "Do not force end ranges, bounce, skip the reverse order, rotate away from the front leg, omit a side, hyperextend the front knee, or add unrelated yoga poses.",
        "frames_count": 16,
    },
    160: {
        "start": "Lie face down, fully visible from head to feet, legs extended and relaxed, forehead hovering just above the floor, neck long, and both arms reaching straight overhead in line with the body.",
        "frames": [
            "Opening prone position with arms overhead and forehead hovering.",
            "Lift both straight arms only slightly off the floor without lifting the head.",
            "Begin sweeping the arms outward while bending the elbows.",
            "Reach a symmetrical W shape: elbows bent beside the upper torso and shoulder blades drawn down and together.",
            "Hold the W briefly with neck long and pelvis grounded.",
            "Sweep the arms forward out of the W.",
            "Reach both arms overhead again while still slightly lifted.",
            "Lower the arms with control to the exact opening pose.",
        ],
        "camera": "Fixed elevated rear three-quarter view, wide enough to show the full body and clearly reveal the overhead-to-W arm path and shoulder blades.",
        "details": "The arms hover only slightly; movement comes from the shoulders and shoulder blades. Keep the neck long, forehead low, pelvis and legs on the floor, and W shape symmetrical.",
        "avoid": "Do not perform a superman lift, raise the legs, crank the head upward, arch the lower back, turn palms into impossible positions, lose arm symmetry, or crop hands.",
        "frames_count": 8,
    },
    161: {
        "start": "Stand facing the camera with feet slightly wider than hip-width, toes naturally forward or slightly outward, heels grounded, torso tall, and arms relaxed.",
        "frames": [
            "Neutral standing stance.",
            "Send hips back and begin a comfortable shallow squat while both arms reach forward at shoulder height.",
            "Shallow squat endpoint with heels down, knees tracking with toes, chest lifted, and arms forward.",
            "Begin standing through both feet while arms start to arc upward.",
            "Stand tall with both arms reaching overhead without excessive back arch.",
            "Lower the arms to the exact neutral opening stance for the loop.",
        ],
        "camera": "Fixed front full-body view, wide enough to show both heels and both hands overhead.",
        "details": "Use an accessible shallow range. Keep both heels grounded, hips moving back, knees aligned, and the transition from forward reach to overhead reach smooth.",
        "avoid": "Do not squat deeply, jump, lift the heels, collapse the knees inward, round the back, add weights, crop hands or feet, or change camera angle.",
        "frames_count": 6,
    },
    162: {
        "start": "Sit upright on the floor facing the camera in a comfortable cross-legged or easy bent-leg position, pelvis level, spine tall, and hands resting near the thighs.",
        "frames": [
            "Tall neutral seated posture.",
            "Reach both hands forward with a long spine, without collapsing the chest.",
            "Return fully to tall neutral.",
            "Reach diagonally toward the right while gently rotating through the upper back.",
            "Return to tall neutral.",
            "Reach the right arm overhead with a gentle rightward upper-back rotation, hips grounded.",
            "Return to tall neutral.",
            "Reach diagonally toward the left with gentle upper-back rotation.",
            "Return to tall neutral.",
            "Reach the left arm overhead with gentle leftward upper-back rotation.",
            "Return to tall neutral with both hands near the thighs.",
            "Hold the exact opening posture for a seamless loop.",
        ],
        "camera": "Fixed front full-body seated view, slightly elevated so forward and diagonal reach directions are distinct and overhead hands remain visible.",
        "details": "Clearly separate forward, diagonal, and overhead reaches. Return to a tall posture between every reach and show both rotational directions while the pelvis remains grounded.",
        "avoid": "Do not kneel, stand, turn this into a side bend only, round deeply through the lower back, skip neutral resets, omit one direction, or crop hands.",
        "frames_count": 12,
    },
    163: {
        "start": "Sit tall on the floor facing the camera, knees bent, feet lightly planted in front, trunk braced, and both hands held lightly near the chest in a relaxed guard.",
        "frames": [
            "Opening seated guard with both feet centered.",
            "Reach the right hand forward while the left toes tap forward lightly; torso stays tall.",
            "Return right hand and left foot to the opening guard.",
            "Reach the left hand forward while the right toes tap forward.",
            "Return to guard.",
            "Repeat a right-hand forward reach with left toe tap.",
            "Return to guard.",
            "On the fourth count, perform a controlled side reach to the left while maintaining the seated base; do not collapse.",
            "Return to guard and begin the mirrored sequence with left hand and right toe leading.",
            "Alternate the opposite hand-and-toe pairing once more.",
            "On the mirrored fourth count, perform a controlled side reach to the right.",
            "Return exactly to the opening seated guard for the loop.",
        ],
        "camera": "Fixed straight-on full-body seated view, wide enough to show both forward toe taps, both side reaches, hands, and feet.",
        "details": "Each forward hand reach pairs with the opposite-side toe tap. A controlled side reach appears every fourth count. Keep breathing steady and the torso tall.",
        "avoid": "Do not perform V-ups, bicycle crunches, punches, high kicks, deep trunk twisting, simultaneous same-side hand and toe, omit the side reaches, or crop feet.",
        "frames_count": 12,
    },
    164: {
        "start": "Sit on the floor facing the camera, both knees bent, feet flat and set wider than the hips, hands lightly on the floor behind or beside the hips only for comfortable support, and torso tall.",
        "frames": [
            "Opening center position with knees upright and feet wide.",
            "Both knees begin lowering together toward the right as the hips rotate internally and externally.",
            "Right-side 90/90 endpoint within a comfortable range; torso remains tall.",
            "Drive through the hips to bring both knees back through center.",
            "Both knees begin lowering together toward the left.",
            "Left-side 90/90 endpoint with both sit bones as comfortable as possible.",
            "Drive back through center slowly.",
            "Match the opening knees-up position exactly for the loop.",
        ],
        "camera": "Fixed front, slightly elevated full-body seated view so both knee arcs, foot placement, and tall torso are visible.",
        "details": "Both knees travel together from side to side while the feet stay wider than the hips. Keep the torso tall and use a slow, unforced hip range.",
        "avoid": "Do not lift the feet and swing them, collapse the chest, force knees to the floor, move only one knee, perform a seated spinal twist, crop the feet, or change viewpoint.",
        "frames_count": 8,
    },
    165: {
        "start": "Lie on the back facing upward, knees bent together, feet flat and close, arms open in a T at shoulder height with palms up, and both shoulders relaxed on the floor.",
        "frames": [
            "Opening supine center position with knees pointing upward.",
            "Both knees begin lowering together toward the right while shoulders remain down.",
            "Comfortable right-side endpoint with slow exhale and no forced floor contact.",
            "Return both knees through center using the trunk gently.",
            "Both knees begin lowering together toward the left.",
            "Comfortable left-side endpoint while both shoulders stay relaxed toward the floor.",
            "Return through center slowly.",
            "Match the opening center position exactly for a seamless loop.",
        ],
        "camera": "Fixed overhead full-body view, centered on the torso and wide enough to show both hands, knees, and feet throughout.",
        "details": "Knees move together as one unit. Alternate both sides, move slowly with an exhale, and prioritize keeping both shoulders relaxed toward the floor.",
        "avoid": "Do not show only one side, lift a shoulder aggressively, separate the knees, straighten the legs, turn it into a bicycle motion, rotate the camera, or crop arms.",
        "frames_count": 8,
    },
    166: {
        "start": "Begin on hands and knees, wrists under shoulders and knees under hips, spine neutral, hands shoulder-width, and toes relaxed.",
        "frames": [
            "Opening quadruped position.",
            "Send the hips gently backward toward the heels while both hands stay planted forward.",
            "Reach a comfortable child-pose-like center stretch without forcing the hips to the heels.",
            "Walk both hands together several small steps toward the right while hips stay back and centered.",
            "Reach the right-side hand position, creating a comfortable stretch along the left side of the torso.",
            "Walk both hands back through center.",
            "Walk both hands together toward the left.",
            "Reach the left-side hand position, stretching the right side body.",
            "Return both hands through center and shift forward toward hands and knees.",
            "Match the opening quadruped pose exactly for the loop.",
        ],
        "camera": "Fixed elevated rear three-quarter full-body view so hand-walking direction, hips, spine, knees, and side-body length are visible.",
        "details": "Both hands walk to the same side together. Hips remain gently toward the heels, movement is comfortable, and both sides are shown with a center return.",
        "avoid": "Do not thread one arm under the body, rotate onto a shoulder, shift the hips sideways, hold the breath, show only one side, lift the knees, or crop hands.",
        "frames_count": 10,
    },
    167: {
        "start": "Begin in a high plank in side profile, palms beneath shoulders, trunk braced, legs straight, feet stable, and body aligned from head to heels.",
        "frames": [
            "Opening high plank.",
            "First third of the three-second eccentric lowering; elbows angle backward.",
            "Second third of the lowering with chest moving toward the floor and hips aligned.",
            "Final controlled lowering until the torso reaches the floor.",
            "Place both knees down on the floor after the lowering is complete.",
            "With knees down, reposition safely through a hands-and-knees reset rather than pressing up from the toes.",
            "Extend one leg back.",
            "Extend the other leg back to rebuild the high plank.",
            "Stabilize with hands beneath shoulders and trunk braced.",
            "Match the exact opening high plank for the next loop.",
        ],
        "camera": "Fixed full-body side view at low waist height, clearly showing the three-stage descent, elbow angle, floor contact, knees-down reset, and return to plank.",
        "details": "The active work is only the slow lowering. The return must use a knees-down safe reset; do not press back up as a standard push-up.",
        "avoid": "Do not perform repeated normal push-ups, omit the knees-down reset, flare elbows sideways, sag or pike the hips, bounce onto the floor, crop feet, or move the camera.",
        "frames_count": 10,
    },
    169: {
        "start": "Sit tall on the floor facing the camera, knees bent, feet visible and lightly planted, trunk braced, and hands ready near the chest.",
        "frames": [
            "Opening seated ready posture.",
            "First quick cross-body reach: right hand reaches diagonally toward the left side without collapsing the torso.",
            "Return to center.",
            "Second quick cross-body reach: left hand reaches diagonally toward the right side.",
            "Return to center.",
            "First heel tap: extend or slide the right heel forward to tap the floor.",
            "Second heel tap: return right heel and tap the left heel forward.",
            "Return both feet and perform one controlled overhead reach with both arms.",
            "Return to ready posture for the next round.",
            "Reverse the lead: left hand makes the first cross-body reach.",
            "Right hand makes the second cross-body reach after a center reset.",
            "Perform the two heel taps in the reversed lead order.",
            "Perform one overhead reach.",
            "Return exactly to the opening ready posture for the loop.",
        ],
        "camera": "Fixed straight-on full-body seated view, wide enough for diagonal reaches, overhead hands, and both heel taps.",
        "details": "Each round contains exactly two cross-body reaches, two heel taps, and one overhead reach. Reverse the lead side in the second round and keep the order precise.",
        "avoid": "Do not add punches, toe touches, extra taps, a V-sit, large trunk rotation, standing, omitted lead reversal, camera motion, or cropped hands and feet.",
        "frames_count": 14,
    },
    170: {
        "start": "Sit tall on the floor facing the camera, knees bent, feet flat, spine neutral, pelvis level, and arms relaxed near the torso.",
        "frames": [
            "Opening fully upright seated posture.",
            "Lean the straight trunk back slightly as one unit without rounding the lower back.",
            "Reach both arms straight forward together while resisting all trunk rotation.",
            "Return the arms and sit fully upright between rounds.",
            "Lean back slightly again and reach both arms diagonally toward the right while ribs and pelvis continue facing forward.",
            "Return upright without twisting.",
            "Lean back slightly and reach both arms diagonally toward the left while resisting rotation.",
            "Return fully upright.",
            "Settle both arms beside the torso with neutral spine.",
            "Match the exact opening posture for the loop.",
        ],
        "camera": "Fixed front three-quarter full-body seated view so the small backward lean, neutral lumbar spine, diagonal arm directions, and non-rotating pelvis are clear.",
        "details": "The torso remains rigid and neutral. Arm reaches go forward, right diagonal, and left diagonal; the trunk resists following the arms. Return upright between rounds.",
        "avoid": "Do not twist the rib cage, round the lower back, perform Russian twists, lift the feet, recline deeply, reach one arm at a time, omit upright resets, or crop hands.",
        "frames_count": 10,
    },
    172: {
        "start": "Stand tall in side/front three-quarter view, feet about hip-width, arms relaxed, and clear floor space in front.",
        "frames": [
            "Opening standing position.",
            "Squat down with hips back and place both palms flat on the floor.",
            "Step or lightly jump both feet back into a strong high plank.",
            "Lower into one controlled push-up while the trunk stays aligned.",
            "Reach the bottom of the single push-up.",
            "Press back to the high plank.",
            "Step or lightly hop both feet toward the hands into a compact squat.",
            "Lift the hands and begin standing.",
            "Stand fully upright without jumping or reaching overhead.",
            "Match the opening stance exactly for the loop.",
        ],
        "camera": "Fixed wide full-body side/front three-quarter view showing hands, feet, plank alignment, squat, and standing position without any cropping.",
        "details": "Show exactly one push-up. The return ends in a quiet stand with no jump. Hands are planted before the feet travel back.",
        "avoid": "Do not add a burpee jump, overhead clap, second push-up, mountain climber, knee push-up, sagging plank, camera motion, or missing limbs.",
        "frames_count": 10,
    },
    173: {
        "start": "Stand facing the camera in a wide stance, feet planted and toes comfortably turned slightly outward, chest lifted, spine long, and arms forward for balance.",
        "frames": [
            "Wide neutral stance with both knees softly unlocked.",
            "Shift hips toward the right and begin bending the right knee; left leg lengthens.",
            "Comfortable right Cossack endpoint with chest lifted, right knee tracking with toes, and left leg long.",
            "Press through the right foot and travel smoothly back through center.",
            "Shift hips toward the left and begin bending the left knee; right leg lengthens.",
            "Comfortable left Cossack endpoint with chest lifted.",
            "Press through the left foot and return through center.",
            "Match the opening wide stance for a seamless loop.",
        ],
        "camera": "Fixed straight-on full-body view at hip height, wide enough to show both feet and the full lateral travel.",
        "details": "Keep the opposite leg long on each side, chest lifted, depth comfortable, and transitions smooth. Heels remain grounded when the instructor's mobility allows.",
        "avoid": "Do not turn it into side lunges with feet stepping, bounce at depth, force a deep squat, collapse the chest, let knees cave inward, show only one side, or crop feet.",
        "frames_count": 8,
    },
    174: {
        "start": "Stand tall in side profile with feet stable about hip-width, knees soft, arms relaxed, and enough floor in front for a full walkout.",
        "frames": [
            "Opening standing posture.",
            "Hinge forward from the hips, softening the knees as needed, and bring hands toward the floor.",
            "Place both hands down near the feet while the feet remain planted.",
            "Walk the hands forward one at a time.",
            "Continue walking until reaching a strong high plank.",
            "Lower into one controlled push-up with the body aligned.",
            "Press back to the high plank.",
            "Walk the hands backward toward the stationary feet.",
            "Bring hands near the feet and soften the knees.",
            "Begin extending the hips and spine to stand.",
            "Stand fully tall with arms relaxed.",
            "Match the exact opening posture for the loop.",
        ],
        "camera": "Fixed wide full-body side view showing the entire hand-walk distance, stationary feet, plank, push-up, and final stand.",
        "details": "Feet stay in place while the hands walk out and back. Include exactly one controlled push-up and allow soft knees during the hinge.",
        "avoid": "Do not walk the feet, add a jump, omit the push-up, perform extra push-ups, round violently, move the camera, crop hands at full walkout, or change clothing/body proportions.",
        "frames_count": 12,
    },
    175: {
        "start": "Sit in a right-leading 90/90 hip position: right shin in front, left leg folded to the side/back, both knees near 90 degrees, both sit bones comfortable on the floor, spine tall, and hands relaxed.",
        "frames": [
            "Opening right-leading 90/90 seat.",
            "Begin rotating the rib cage toward the right front shin without forcing the hips.",
            "Reach the opposite left arm upward as the rib cage rotates toward the front shin.",
            "Reach the comfortable rotation endpoint with both sit bones grounded.",
            "Lower the arm and return slowly to the upright right-leading seat.",
            "Use a controlled hip switch to rearrange the legs into a left-leading 90/90 position.",
            "Settle both sit bones comfortably with tall posture.",
            "Rotate the rib cage toward the left front shin.",
            "Reach the opposite right arm upward.",
            "Return slowly to the upright left-leading seat.",
            "Switch the legs back toward the right-leading arrangement.",
            "Match the exact opening 90/90 posture for the loop.",
        ],
        "camera": "Fixed elevated front three-quarter full-body seated view showing both 90/90 leg arrangements, sit-bone contact, rib-cage rotation, and overhead arm.",
        "details": "Rotate toward the front shin and reach the opposite arm up. Complete both sides without forcing hip range or aggressively lifting a sit bone.",
        "avoid": "Do not rotate away from the front shin, reach the same-side arm, lift into a kneel, force knees flat, show only one side, collapse the spine, or crop the overhead hand.",
        "frames_count": 12,
    },
    176: {
        "start": "Begin on hands and knees, wrists under shoulders, knees under hips, spine neutral, hips centered and level, and head aligned with the spine.",
        "frames": [
            "Opening quadruped position.",
            "Slide the right arm palm-up beneath the left arm across the floor while the hips remain centered.",
            "Reach the right-threaded endpoint with gentle upper-back rotation and right shoulder near the floor.",
            "Unthread the right arm back through center.",
            "Sweep the right arm upward toward the ceiling, rotating gently through the upper back.",
            "Return the right hand beneath the shoulder.",
            "Slide the left arm beneath the right arm across the floor.",
            "Reach the left-threaded endpoint with hips still centered.",
            "Unthread the left arm.",
            "Sweep the left arm upward toward the ceiling.",
            "Return the left hand beneath the shoulder.",
            "Match the opening quadruped pose exactly for the loop.",
        ],
        "camera": "Fixed front three-quarter view from slightly above, wide enough to show both hands, knees, centered hips, under-body slides, and ceiling reaches.",
        "details": "Each side includes both phases: arm threads beneath the other arm, then the same arm sweeps upward. Both knees stay grounded and hips remain centered.",
        "avoid": "Do not show only one side, shift the hips sideways, lift a knee, turn it into a side plank, omit the upward sweep, force neck rotation, crop hands, or move the camera.",
        "frames_count": 12,
    },
}


def prompt_for(exercise: dict, spec: dict) -> str:
    instructions = "\n".join(
        f"{index}. {instruction}"
        for index, instruction in enumerate(exercise["instructions"], start=1)
    )
    frames = "\n".join(
        f"Frame {index}: {description}"
        for index, description in enumerate(spec["frames"], start=1)
    )
    support = spec.get(
        "support",
        "Database equipment list: none. Do not add weights, bands, benches, or machines.",
    )
    filename = f"{exercise['id']}-{exercise['name'].lower().replace(' ', '-').replace('/', '-')}.gif"
    return f"""Create an original, high-quality exercise demonstration for LockIn.

EXERCISE ID AND EXACT NAME
{exercise['id']} — {exercise['name']}

ORIGINAL DATABASE INSTRUCTIONS — COPY AND FOLLOW EXACTLY
{instructions}

REQUIRED EQUIPMENT
{support}

STARTING POSITION
{spec['start']}

EXACT ANIMATION FRAME SEQUENCE
Use {spec['frames_count']} distinct key frames in this order, with smooth in-between motion:
{frames}

ENDING POSITION AND LOOP
The last frame must flow naturally back into Frame 1. Preserve the instructor's location, scale, orientation, clothing, anatomy, lighting, and background so the loop has no visual jump.

CAMERA
{spec['camera']} The camera must remain completely fixed: no cuts, zoom, pan, orbit, reframing, or background shift.

MOVEMENT ACCURACY
{spec['details']}

COMMON GENERATION ERRORS TO AVOID
{spec['avoid']} Never add extra limbs or fingers, merge limbs, distort joints, swap left and right unexpectedly, change body proportions, change clothing, change the environment, or show impossible joint motion.

VISUAL STYLE
One anatomically consistent adult fitness instructor in simple unbranded athletic clothing and training shoes where appropriate. Use a clean, polished fitness-instruction style on a plain pale neutral background with soft even lighting. Keep the full movement visible; include the complete body whenever the exercise uses the whole body. No other people. No unrelated props.

GIF OUTPUT REQUIREMENTS
- Output a REAL animated GIF file, not a static PNG, JPG, WEBP, poster, contact sheet, storyboard, or a still image renamed with a .gif extension.
- Use {spec['frames_count']} distinct key frames plus smooth interpolation where supported.
- Seamless infinite loop; fixed camera; stable background.
- Same adult instructor, face, hairstyle, clothing, body proportions, limb lengths, and environment across every frame.
- Smooth, realistic speed and anatomically possible transitions.
- Accurate hands, arms, legs, feet, joint alignment, and contact with the floor or chair.
- No text, labels, arrows, captions, borders, logos, or watermarks.
- Square 1:1 canvas, preferably 512×512 or larger; optimize for a website preview while preserving clear anatomy.
- Expected filename: {filename}
- Before returning the result, verify that the file is genuinely animated and contains multiple visually distinct frames. If true animated-GIF output is unavailable, say so clearly instead of returning a static image.
"""


def main() -> None:
    exercises_by_id = {exercise["id"]: exercise for exercise in exercises}
    assert set(MISSING_IDS) == set(SPECS)
    lines = [
        "# ChatGPT prompts for LockIn's 24 missing exercise GIFs",
        "",
        "Generated from the live `exercises.py` and `exercise_media.py` state. Each fenced block is standalone and copy-paste-ready. Submit one block per generation request.",
        "",
        "> Important: ChatGPT image generation may return a static image even when asked for animation. Accept a result only if the downloaded file is a genuine multi-frame GIF and the complete movement passes visual review.",
        "",
    ]
    for exercise_id in MISSING_IDS:
        exercise = exercises_by_id[exercise_id]
        lines.extend([
            f"## {exercise_id} — {exercise['name']}",
            "",
            "```text",
            prompt_for(exercise, SPECS[exercise_id]).rstrip(),
            "```",
            "",
        ])
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
