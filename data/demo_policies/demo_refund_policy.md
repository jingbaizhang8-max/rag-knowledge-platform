
# Demo Store Return and Refund Policy

IMPORTANT: This is a fictional demonstration policy for AI engineering tests.
It is not an official Olist policy or a policy of any real merchant.
It must not be used to determine refund eligibility for real Olist orders.

## 1. Return Request Window

For this fictional demo store, customers may request a return
within 14 calendar days after the confirmed delivery date.

## 2. Return Conditions

The customer must provide a valid order ID.

Items should be unused and in their original condition,
except when the item arrived damaged or defective.

A return request does not guarantee a refund.
All requests are subject to eligibility review.

## 3. Damaged or Incorrect Items

Customers who receive damaged, defective, or incorrect items
should contact customer support and provide relevant evidence.

Customer support may request photos or other supporting details.

## 4. Refund Processing

For this fictional store, an approved refund is issued to
the original payment method within 5 business days after
the returned item has been inspected and approved.

Payment-provider processing time may vary.

## 5. Human Review

If the delivery date, item condition, or eligibility cannot
be verified, the AI assistant must not promise a refund.

The request must be referred to a human support representative.

## 6. AI Agent Restrictions

The AI assistant can explain the demo policy and help users
understand the return process.

The AI assistant must not issue real refunds, approve payments,
or invent policy terms or tracking numbers.


# Demo Store Return and Refund Policy V2

IMPORTANT:
This is a fictional policy for AI engineering demonstrations.
It is NOT an official Olist policy.
Olist historical order data is used only for backend testing.
No real money is transferred in this project.

## 1. Return Request Window

Customers may request a return within 14 calendar days
after the confirmed delivery date.

A return request does not guarantee approval.

If the delivery date cannot be verified, the request
must be reviewed by a human support representative.

## 2. Orders Not Yet Shipped

If an order has not been shipped, the customer may
request cancellation and a simulated refund.

The system must verify the customer's identity
and ownership of the order.

The request must be reviewed before approval.

The AI assistant cannot automatically cancel an order
or execute a refund.

## 3. Shipped or In-Transit Orders

If an order has already shipped or is currently
in transit, the customer may still submit
a return or refund request.

However, a shipped order is NOT automatically
eligible for an approved refund.

The request must be reviewed by a human representative.

For returns subject to the normal 14-day window,
the window begins after confirmed delivery.

If the delivery status is unknown or incomplete,
the AI assistant must not assume eligibility.

## 4. Return Conditions

Customers must provide a valid order ID.

Items should normally be unused and in their
original condition.

Exceptions may apply to damaged, defective,
or incorrect items.

All requests are subject to eligibility review.

## 5. Damaged, Defective, or Incorrect Items

Customers may submit a support request if
an item arrives damaged, defective, or incorrect.

The customer may be asked to provide photos
or supporting evidence.

A human reviewer determines the appropriate
resolution.

## 6. Human Review Workflow

Customers must explicitly confirm the creation
of a refund request.

A refund request creates a ticket with status:

pending_review

Only an authorized reviewer may approve or
reject the request.

Possible review results:

approved
rejected

The reviewer must provide a reason.

The system must persist the review decision
and audit record in PostgreSQL.

## 7. Simulated Refund Processing

After a refund ticket is approved, the backend
may execute a simulated refund operation.

The backend must verify:

- The ticket has been approved.
- The order and request are valid.
- The simulated refund has not already been completed.
- The operation passes idempotency checks.

A successful simulation records:

refund_status = completed

The refund record must be saved to PostgreSQL.

The React frontend displays:

"Simulated refund completed.
No real money was transferred."

This operation does NOT contact a payment gateway,
bank, or external payment provider.

## 8. Rejected Requests

If the reviewer rejects a refund request,
the ticket status becomes rejected.

The rejection reason must be stored.

A rejected request cannot trigger
simulated refund completion.

## 9. AI Agent Restrictions

The AI assistant may:

- Explain the fictional demo refund policy.
- Retrieve an authenticated customer's order details.
- Explain shipping and return conditions.
- Guide the customer through submitting a ticket.
- Retrieve the status of an existing ticket.

The AI assistant must NOT:

- Promise automatic refund approval.
- Bypass customer identity verification.
- Bypass human review.
- Claim that real money was refunded.
- Invent eligibility rules or delivery dates.

## 10. Missing Information

If order ownership, delivery information,
item condition, or policy eligibility
cannot be verified, the AI assistant must
explain the uncertainty and recommend
human review.

The assistant must never invent missing facts.

## 11. Example Questions

Q: Can I request a refund if my order has shipped?
A: Yes, you may submit a request, but approval
requires human review. Shipping does not
guarantee refund eligibility.

Q: 我的订单已经发货，还可以申请退款吗？
A: 可以提交退款申请，但需要人工审核。
已发货不代表一定符合退款条件。

Q: Can I cancel an order that has not shipped?
A: You may request cancellation and a simulated
refund, subject to verification and human approval.

Q: How long after delivery can I request a return?
A: Within 14 calendar days after confirmed delivery,
subject to eligibility review.

Q: What happens after approval?
A: The backend may record a completed simulated refund.
No real funds are transferred.

Q: Can the AI automatically approve my refund?
A: No. Only an authorized human reviewer can approve
or reject a refund request.