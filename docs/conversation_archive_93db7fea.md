# POS System Database Isolation (Previous)
**Conversation ID:** 93db7fea-6d7c-4e86-be46-ef1d38be588f

## Summary
The goal of this conversation was to design a Field Sales (POS) Module isolated from the main customer database.

## Architectural Decisions
1.  **Database Isolation:**
    *   Use `pos_sales` table instead of main `sales` table.
    *   Snapshot customer details (Name/Email) to avoid FK relation to real `customers`.
    *   Use Simulation Store (ID: 9999).
2.  **Frontend Logic:**
    *   Role-based UI access (Mobile -> POS, Desktop -> Dashboard).
    *   Offline handling via `localStorage` queue.

## Status at End of Conversation
*   **Planning:** Completed (`POS_UYGULAMA_PLANI.md` updated).
*   **Implementation:** None (No DB tables, API, or UI code written).
