// static/js/persian-datepicker.js
class PersianDatePicker {
    constructor(inputElement, options = {}) {
        this.input = inputElement;
        this.options = Object.assign({
            autoClose: true,
            format: 'YYYY/MM/DD',
            position: 'bottom'
        }, options);

        this.isOpen = false;
        this.currentDate = this.today();
        this.selectedDate = null;

        this.init();
    }

    init() {
        // ایجاد المان تقویم
        this.createCalendar();

        // اضافه کردن event listener به input
        this.input.addEventListener('focus', () => this.open());
        this.input.addEventListener('click', () => this.open());

        // بستن تقویم وقتی کلیک خارج شد
        document.addEventListener('click', (e) => {
            if (!this.calendar.contains(e.target) && e.target !== this.input) {
                this.close();
            }
        });
    }

    createCalendar() {
        this.calendar = document.createElement('div');
        this.calendar.className = 'persian-datepicker';
        this.calendar.style.cssText = `
            position: absolute;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            min-width: 300px;
            display: none;
        `;

        document.body.appendChild(this.calendar);
        this.render();
    }

    render() {
        const [year, month] = this.currentDate;

        this.calendar.innerHTML = `
            <div class="pdp-header" style="padding: 1rem; border-bottom: 1px solid #e2e8f0; background: #f7fafc;">
                <div class="pdp-navigation" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <button type="button" class="pdp-prev-year" style="background: none; border: none; cursor: pointer; padding: 0.25rem; border-radius: 0.25rem; hover:bg-gray-200">
                        <i class="fas fa-angle-double-right"></i>
                    </button>
                    <button type="button" class="pdp-prev-month" style="background: none; border: none; cursor: pointer; padding: 0.25rem; border-radius: 0.25rem; hover:bg-gray-200">
                        <i class="fas fa-angle-right"></i>
                    </button>
                    <div class="pdp-current" style="font-weight: bold; font-size: 1.1rem;">
                        ${this.getMonthName(month)} ${year}
                    </div>
                    <button type="button" class="pdp-next-month" style="background: none; border: none; cursor: pointer; padding: 0.25rem; border-radius: 0.25rem; hover:bg-gray-200">
                        <i class="fas fa-angle-left"></i>
                    </button>
                    <button type="button" class="pdp-next-year" style="background: none; border: none; cursor: pointer; padding: 0.25rem; border-radius: 0.25rem; hover:bg-gray-200">
                        <i class="fas fa-angle-double-left"></i>
                    </button>
                </div>
            </div>
            <div class="pdp-body" style="padding: 1rem;">
                <div class="pdp-weekdays" style="display: grid; grid-template-columns: repeat(7, 1fr; gap: 0.25rem; margin-bottom: 0.5rem;">
                    ${this.getWeekDays().map(day => `
                        <div style="text-align: center; font-size: 0.75rem; color: #718096; font-weight: bold; padding: 0.5rem;">
                            ${day}
                        </div>
                    `).join('')}
                </div>
                <div class="pdp-days" style="display: grid; grid-template-columns: repeat(7, 1fr; gap: 0.25rem;">
                    ${this.getDaysGrid(year, month).map(day => `
                        <button type="button" class="pdp-day ${day.classes}"
                                style="background: ${day.isCurrentMonth ? 'white' : '#f7fafc'};
                                       border: 1px solid ${day.isToday ? '#3b82f6' : 'transparent'};
                                       color: ${day.isCurrentMonth ? (day.isToday ? '#3b82f6' : '#2d3748') : '#a0aec0'};
                                       cursor: pointer;
                                       padding: 0.5rem;
                                       border-radius: 0.25rem;
                                       font-size: 0.875rem;
                                       ${day.isSelected ? 'background: #3b82f6; color: white;' : ''}"
                                data-date="${day.date}">
                            ${day.day}
                        </button>
                    `).join('')}
                </div>
            </div>
            <div class="pdp-footer" style="padding: 1rem; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between;">
                <button type="button" class="pdp-today" style="background: #3b82f6; color: white; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem; cursor: pointer;">
                    امروز
                </button>
                <button type="button" class="pdp-close" style="background: #718096; color: white; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem; cursor: pointer;">
                    بستن
                </button>
            </div>
        `;

        this.attachEvents();
    }

    getWeekDays() {
        return ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج'];
    }

    getMonthName(month) {
        const months = [
            'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
            'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
        ];
        return months[month - 1];
    }

    getDaysGrid(year, month) {
        const days = [];
        const firstDay = this.firstDayOfMonth(year, month);
        const daysInMonth = this.daysInMonth(year, month);
        const daysInPrevMonth = this.daysInMonth(year, month - 1);

        // روزهای ماه قبل
        for (let i = firstDay - 1; i >= 0; i--) {
            days.push({
                day: daysInPrevMonth - i,
                date: this.formatDate(year, month - 1, daysInPrevMonth - i),
                isCurrentMonth: false,
                isToday: false,
                isSelected: false,
                classes: 'pdp-day-other'
            });
        }

        // روزهای ماه جاری
        const today = this.today();
        for (let i = 1; i <= daysInMonth; i++) {
            const isToday = year === today[0] && month === today[1] && i === today[2];
            const isSelected = this.selectedDate &&
                              year === this.selectedDate[0] &&
                              month === this.selectedDate[1] &&
                              i === this.selectedDate[2];

            days.push({
                day: i,
                date: this.formatDate(year, month, i),
                isCurrentMonth: true,
                isToday: isToday,
                isSelected: isSelected,
                classes: `pdp-day-current ${isToday ? 'pdp-day-today' : ''} ${isSelected ? 'pdp-day-selected' : ''}`
            });
        }

        // روزهای ماه بعد
        const totalCells = 42; // 6 هفته
        const remaining = totalCells - days.length;
        for (let i = 1; i <= remaining; i++) {
            days.push({
                day: i,
                date: this.formatDate(year, month + 1, i),
                isCurrentMonth: false,
                isToday: false,
                isSelected: false,
                classes: 'pdp-day-other'
            });
        }

        return days;
    }

    firstDayOfMonth(year, month) {
        // محاسبه روز اول ماه (0=شنبه, 6=جمعه)
        const date = new Date(this.jalaliToGregorian(year, month, 1));
        return date.getDay();
    }

    daysInMonth(year, month) {
        const months = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29];
        if (month === 12 && this.isLeapYear(year)) {
            return 30;
        }
        return months[month - 1];
    }

    isLeapYear(year) {
        // محاسبه سال کبیسه
        return (((year - 474) % 128) <= 29) ?
               (((year - 474) % 128) <= 5) :
               (((year - 474) % 128) === 0);
    }

    today() {
        const now = new Date();
        const jalali = this.gregorianToJalali(now.getFullYear(), now.getMonth() + 1, now.getDate());
        return jalali;
    }

    formatDate(year, month, day) {
        return `${year}/${month.toString().padStart(2, '0')}/${day.toString().padStart(2, '0')}`;
    }

    // توابع تبدیل تاریخ (همان‌هایی که قبلاً داشتیم)
    gregorianToJalali(gy, gm, gd) {
        var g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
        var jy = (gy <= 1600) ? 0 : 979;
        gy -= (gy <= 1600) ? 621 : 1600;
        var gy2 = (gm > 2) ? (gy + 1) : gy;
        var days = (365 * gy) + (parseInt((gy2 + 3) / 4)) - (parseInt((gy2 + 99) / 100)) + (parseInt((gy2 + 399) / 400)) - 80 + gd + g_d_m[gm - 1];
        jy += 33 * (parseInt(days / 12053));
        days %= 12053;
        jy += 4 * (parseInt(days / 1461));
        days %= 1461;
        jy += parseInt((days - 1) / 365);
        if (days > 365) days = (days - 1) % 365;
        var jm = (days < 186) ? 1 + parseInt(days / 31) : 7 + parseInt((days - 186) / 30);
        var jd = 1 + ((days < 186) ? (days % 31) : ((days - 186) % 30));
        return [jy, jm, jd];
    }

    jalaliToGregorian(jy, jm, jd) {
        jy += 1595;
        var days = -355668 + (365 * jy) + (parseInt(jy / 33) * 8) + parseInt(((jy % 33) + 3) / 4) + jd + ((jm < 7) ? (jm - 1) * 31 : ((jm - 7) * 30) + 186);
        var gy = 400 * parseInt(days / 146097);
        days %= 146097;
        if (days > 36524) {
            gy += 100 * parseInt(--days / 36524);
            days %= 36524;
            if (days >= 365) days++;
        }
        gy += 4 * parseInt(days / 1461);
        days %= 1461;
        if (days > 365) {
            gy += parseInt((days - 1) / 365);
            days = (days - 1) % 365;
        }
        var gd = days + 1;
        var sal_a = [0, 31, ((gy % 4 === 0 && gy % 100 !== 0) || (gy % 400 === 0)) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        var gm;
        for (gm = 0; gm < 13; gm++) {
            var v = sal_a[gm];
            if (gd <= v) break;
            gd -= v;
        }
        return new Date(gy, gm - 1, gd);
    }

    attachEvents() {
        // navigation
        this.calendar.querySelector('.pdp-prev-year').addEventListener('click', () => this.navigateYear(-1));
        this.calendar.querySelector('.pdp-prev-month').addEventListener('click', () => this.navigateMonth(-1));
        this.calendar.querySelector('.pdp-next-month').addEventListener('click', () => this.navigateMonth(1));
        this.calendar.querySelector('.pdp-next-year').addEventListener('click', () => this.navigateYear(1));

        // روزها
        this.calendar.querySelectorAll('.pdp-day').forEach(day => {
            day.addEventListener('click', () => this.selectDate(day.dataset.date));
        });

        // دکمه‌های footer
        this.calendar.querySelector('.pdp-today').addEventListener('click', () => this.selectToday());
        this.calendar.querySelector('.pdp-close').addEventListener('click', () => this.close());
    }

    navigateMonth(direction) {
        let [year, month] = this.currentDate;
        month += direction;

        if (month > 12) {
            month = 1;
            year++;
        } else if (month < 1) {
            month = 12;
            year--;
        }

        this.currentDate = [year, month, 1];
        this.render();
        this.positionCalendar();
    }

    navigateYear(direction) {
        let [year, month] = this.currentDate;
        year += direction;
        this.currentDate = [year, month, 1];
        this.render();
        this.positionCalendar();
    }

    selectDate(dateString) {
        this.selectedDate = dateString.split('/').map(Number);
        this.input.value = dateString;

        if (this.options.autoClose) {
            this.close();
        }

        // trigger change event
        this.input.dispatchEvent(new Event('change', { bubbles: true }));
    }

    selectToday() {
        const today = this.today();
        this.selectDate(this.formatDate(...today));
    }

    open() {
        if (this.isOpen) return;

        this.isOpen = true;
        this.calendar.style.display = 'block';
        this.positionCalendar();
    }

    close() {
        this.isOpen = false;
        this.calendar.style.display = 'none';
    }

    positionCalendar() {
        const rect = this.input.getBoundingClientRect();
        this.calendar.style.top = (rect.bottom + window.scrollY) + 'px';
        this.calendar.style.left = (rect.left + window.scrollX) + 'px';
    }
}

// ثبت به صورت global
window.PersianDatePicker = PersianDatePicker;