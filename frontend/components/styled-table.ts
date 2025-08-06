/* -------------------------------------------------------------------------- */

export interface StyledTableAttributes {
    // ...
}

/* -------------------------------------------------------------------------- */

export class StyledTable extends HTMLTableElement implements StyledTableAttributes {

    constructor() {
        super();
    }
}

/* -------------------------------------------------------------------------- */

customElements.define('styled-table', StyledTable);

/* -------------------------------------------------------------------------- */
