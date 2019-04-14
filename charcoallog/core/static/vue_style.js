Vue.component('core_line1', {
    props: ['key_', 'val'],
    template:`
        <td align="center">
            <b>{{ key_ }} </b> <br>
            <font size="2">
            <span :style="style">{{ val }}</span>
            </font>
        </td>
    `,
    //data: function() {
    //    return {
    //        k: this.key_,
    //        vl: this.val,
    //    }
    //},
    computed: {
        style() {
            var font_color = 'black';
            if (this.val < 0)
                font_color = 'red';
            return {
                color: font_color,
            };
        },
    },
});

var core_line1 = new Vue({
    el: "#core_line1_accounts",
    data: {
        out: '',
    },
});