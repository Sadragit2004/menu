// تابع برای ثبت بازدید یکتا از منوی رستوران
class MenuViewTracker {
    constructor() {
        this.restaurantSlug = this.getRestaurantSlug();
        this.isViewRecorded = false;
        this.init();
    }

    // استخراج اسلاگ رستوران از URL
    getRestaurantSlug() {
        const path = window.location.pathname;
        const slugMatch = path.match(/\/menu\/([^\/]+)/);
        return slugMatch ? slugMatch[1] : null;
    }

    // دریافت session key
    getSessionKey() {
        // اگر session storage موجود است از آن استفاده کن
        if (typeof sessionStorage !== 'undefined') {
            let sessionKey = sessionStorage.getItem('menu_session_key');
            if (!sessionKey) {
                sessionKey = this.generateSessionKey();
                sessionStorage.setItem('menu_session_key', sessionKey);
            }
            return sessionKey;
        }
        // در غیر این صورت یک کلید سشن ساده ایجاد کن
        return this.generateSessionKey();
    }

    // تولید کلید سشن یکتا
    generateSessionKey() {
        return 'menu_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // دریافت IP کاربر
    async getClientIP() {
        try {
            const response = await fetch('https://menu/api.ipify.org?format=json');
            const data = await response.json();
            return data.ip;
        } catch (error) {
            console.log('Could not get IP address:', error);
            return null;
        }
    }

    // ثبت بازدید
    async recordMenuView() {
        if (!this.restaurantSlug || this.isViewRecorded) {
            return;
        }

        try {
            const sessionKey = this.getSessionKey();
            const userAgent = navigator.userAgent;
            const ipAddress = await this.getClientIP();

            const response = await fetch(`/menu/api/restaurant/${this.restaurantSlug}/menu/view/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    session_key: sessionKey,
                    user_agent: userAgent,
                    ip_address: ipAddress
                })
            });

            const data = await response.json();

            if (data.success) {
                this.isViewRecorded = true;
                console.log('Menu view recorded:', data);

                // آپدیت آمار در صورت نیاز
                if (data.stats) {
                    this.updateViewStats(data.stats);
                }
            } else {
                console.warn('Failed to record menu view:', data.message);
            }

        } catch (error) {
            console.error('Error recording menu view:', error);
        }
    }

    // دریافت آمار بازدید
    async getMenuViewStats() {
        if (!this.restaurantSlug) {
            return;
        }

        try {
            const response = await fetch(`/menu/api/restaurant/${this.restaurantSlug}/menu/stats/`);
            const data = await response.json();

            if (data.success) {
                this.updateViewStats(data.stats);
            }

            return data;
        } catch (error) {
            console.error('Error fetching menu view stats:', error);
            return null;
        }
    }

    // آپدیت آمار در صفحه (اختیاری)
    updateViewStats(stats) {
        // اگر المان‌هایی برای نمایش آمار دارید، اینجا آپدیت کنید
        const statsElement = document.getElementById('view-stats');
        if (statsElement) {
            statsElement.innerHTML = `
                <div class="view-stat-item">
                    <span class="stat-label">بازدید امروز:</span>
                    <span class="stat-value">${stats.daily_views}</span>
                </div>
                <div class="view-stat-item">
                    <span class="stat-label">کل بازدیدها:</span>
                    <span class="stat-value">${stats.total_views}</span>
                </div>
            `;
        }

        // همچنین می‌توانید در کنسول لاگ کنید
        console.log('Menu View Stats:', stats);
    }

    // دریافت CSRF token
    getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

    // بررسی عمق اسکرول کاربر
    initScrollTracking() {
        let maxScrollDepth = 0;
        let scrollTimeout;

        const trackScrollDepth = () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollPercentage = scrollHeight > 0 ? Math.round((scrollTop / scrollHeight) * 100) : 0;

            if (scrollPercentage > maxScrollDepth) {
                maxScrollDepth = scrollPercentage;

                // ارسال داده‌های اسکرول به سرور (اختیاری)
                this.trackScrollDepth(maxScrollDepth);
            }
        };

        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(trackScrollDepth, 100);
        });
    }

    // ارسال داده‌های اسکرول (اختیاری)
    async trackScrollDepth(depth) {
        try {
            await fetch(`/menu/api/restaurant/${this.restaurantSlug}/menu/scroll/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    scroll_depth: depth,
                    session_key: this.getSessionKey()
                })
            });
        } catch (error) {
            console.log('Error tracking scroll depth:', error);
        }
    }

    // رهگیری زمان ماندگاری کاربر
    initTimeTracking() {
        let startTime = Date.now();

        window.addEventListener('beforeunload', () => {
            const endTime = Date.now();
            const timeSpent = Math.round((endTime - startTime) / 1000); // به ثانیه

            this.trackTimeSpent(timeSpent);
        });
    }

    // ارسال زمان ماندگاری (اختیاری)
    async trackTimeSpent(seconds) {
        try {
            await fetch(`/menu/api/restaurant/${this.restaurantSlug}/menu/time/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    time_spent: seconds,
                    session_key: this.getSessionKey()
                })
            });
        } catch (error) {
            console.log('Error tracking time spent:', error);
        }
    }

    // مقداردهی اولیه
    async init() {
        if (!this.restaurantSlug) {
            console.warn('Restaurant slug not found');
            return;
        }

        // ثبت بازدید بلافاصله پس از لود صفحه
        await this.recordMenuView();

        // دریافت آمار
        await this.getMenuViewStats();

        // فعال کردن رهگیری اسکرول
        this.initScrollTracking();

        // فعال کردن رهگیری زمان
        this.initTimeTracking();

        // ثبت بازدید مجدد اگر کاربر بعد از 30 دقیقه برگشت
        this.setupRevisitTracking();
    }

    // رهگیری بازدید مجدد
    setupRevisitTracking() {
        // هر 30 دقیقه یکبار امکان ثبت بازدید مجدد
        setInterval(() => {
            this.isViewRecorded = false;
        }, 30 * 60 * 1000); // 30 دقیقه

        // وقتی کاربر به تب برمی‌گردد
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible' && !this.isViewRecorded) {
                setTimeout(() => {
                    this.recordMenuView();
                }, 1000);
            }
        });
    }
}

// استایل برای نمایش آمار (در صورت نیاز)
const viewStatsStyles = `
.view-stats-container {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background: rgba(0,0,0,0.8);
    color: white;
    padding: 10px;
    border-radius: 8px;
    font-size: 12px;
    z-index: 1000;
    backdrop-filter: blur(10px);
}

.view-stat-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
}

.view-stat-item:last-child {
    margin-bottom: 0;
}

.stat-label {
    color: #ccc;
}

.stat-value {
    color: #fff;
    font-weight: bold;
}
`;

// تابع برای ایجاد المان نمایش آمار
function createViewStatsElement() {
    const style = document.createElement('style');
    style.textContent = viewStatsStyles;
    document.head.appendChild(style);

    const statsDiv = document.createElement('div');
    statsDiv.id = 'view-stats';
    statsDiv.className = 'view-stats-container';
    statsDiv.innerHTML = `
        <div class="view-stat-item">
            <span class="stat-label">بازدید امروز:</span>
            <span class="stat-value">0</span>
        </div>
        <div class="view-stat-item">
            <span class="stat-label">کل بازدیدها:</span>
            <span class="stat-value">0</span>
        </div>
    `;

    document.body.appendChild(statsDiv);
    return statsDiv;
}

// مقداردهی اولیه وقتی صفحه لود شد
document.addEventListener('DOMContentLoaded', function() {
    // ایجاد ترکر بازدید
    window.menuViewTracker = new MenuViewTracker();

    // اگر می‌خواهید آمار نمایش داده شود، این خط را آنکامنت کنید
    // createViewStatsElement();

    console.log('Menu view tracker initialized');
});

// همچنین می‌توانید از طریق رویدادهای دیگر هم بازدید ثبت کنید
// مثلاً وقتی کاربر با غذاها تعامل دارد

// ثبت بازدید وقتی کاربر روی غذا کلیک می‌کند
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(e) {
        if (e.target.closest('.food-card') || e.target.closest('.order-btn')) {
            // اینجا می‌توانید تعامل کاربر با غذاها را هم رهگیری کنید
            console.log('User interacted with food item');
        }
    });
});

// تابع ساده‌تر برای استفاده سریع (اگر نمی‌خواهید از کلاس استفاده کنید)
async function recordSimpleMenuView(restaurantSlug) {
    try {
        const sessionKey = 'menu_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        const userAgent = navigator.userAgent;

        const response = await fetch(`/menu/api/restaurant/${restaurantSlug}/menu/view/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                session_key: sessionKey,
                user_agent: userAgent
            })
        });

        const data = await response.json();

        if (data.success) {
            console.log('View recorded successfully');
            return data;
        }

        return data;
    } catch (error) {
        console.error('Error recording view:', error);
        return { success: false, message: error.message };
    }

    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }
}

// استفاده ساده:
// recordSimpleMenuView('restaurant-slug-here');