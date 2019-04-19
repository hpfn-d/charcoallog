Vue.component('summary-tpl', {
    props: ['k_', 'vl_'],
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
            k: this.k_,
            vl: this.vl_,
        }
    }
})