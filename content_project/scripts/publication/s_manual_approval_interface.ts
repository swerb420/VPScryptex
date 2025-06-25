// /outputs/manual_approval_interface.ts

// This script would be called by a Windmill App where a user reviews a draft.
// The UI would display the draft details (title, video) and have "Approve" and "Reject" buttons.

interface Draft {
  draft_id: string;
  // ... other fields from the draft object
}

type ApprovalDecision = 'approved' | 'rejected';

interface ApprovalResult {
  status: 'success' | 'error';
  message: string;
  draft_id: string;
  decision: ApprovalDecision;
  next_step: 'schedule_post' | 'send_to_rework' | 'none';
}

export async function w_main(
  draft: Draft,
  decision: ApprovalDecision,
  rejection_reason: string = ''
): Promise<ApprovalResult> {
  console.log(`Processing decision for draft ${draft.draft_id}: ${decision}`);

  if (!draft || !draft.draft_id) {
    return {
      status: 'error',
      message: 'Invalid draft object provided.',
      draft_id: 'unknown',
      decision: decision,
      next_step: 'none',
    };
  }

  if (decision === 'approved') {
    // In a real flow, this would trigger the 'post_to_platforms.py' script.
    // pseudo-code:
    // await runScript({ path: "/outputs/post_to_platforms", args: { draft: draft } });

    return {
      status: 'success',
      message: `Draft ${draft.draft_id} approved and sent for posting.`,
      draft_id: draft.draft_id,
      decision: 'approved',
      next_step: 'schedule_post',
    };
  } else if (decision === 'rejected') {
    // In a real flow, this might trigger a notification or a new task for a human.
    // It would also log the rejection reason.
    console.log(`Draft ${draft.draft_id} rejected. Reason: ${rejection_reason}`);

    return {
      status: 'success',
      message: `Draft ${draft.draft_id} rejected. Reason logged.`,
      draft_id: draft.draft_id,
      decision: 'rejected',
      next_step: 'send_to_rework',
    };
  }

  // Fallback for invalid decision
  return {
      status: 'error',
      message: 'Invalid decision provided.',
      draft_id: draft.draft_id,
      decision: decision,
      next_step: 'none',
    };
}

