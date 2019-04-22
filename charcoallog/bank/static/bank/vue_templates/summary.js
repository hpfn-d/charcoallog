Vue.component('summary-tpl', {
    props: ['data'],
    template:`
        <li class="nav-item nav-link text-muted">
           {{ k }}<br>
            <span id="kk">
                {{ vl }}
            </span>
        </li>
    `,
    data: function() {
        return {
            //delimiter: ['[[', ']]'],
            k: this.data.category,
            vl: this.data.val,
        }
    }
})