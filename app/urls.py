from django.urls import path
#from user import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as  auth_views
from . import views
#from .views import CustomerLoginView
#from .views import LoginView, CustomerRegistrationView

from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    #path('', views.home, name="home"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('address/', views.address, name='address'),

    path('about-us/', views.aboutus, name='aboutus'),
    path('about-us2/', views.aboutus2, name='aboutus2'),

    path('influencer_rules/', views.influencer_rules, name='influencer_rules'),

    path('contact-us/', views.contactus, name='contactus'),
    path('contact-us2/', views.contactus2, name='contactus2'),


    path('sendmail/', views.sendmail, name='sendmail'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),




    path('', views.ProductView.as_view(), name="home"),
    path('bottomwears/', views.BottomWear.as_view(), name="bottomwear"),
    path('topwears/', views.TopWear.as_view(), name="topwear"),
    path('tshirts/', views.Tshirts.as_view(), name="tshirts"),
    path('menswear/', views.MensWear.as_view(), name="menswear"),
    path('menswear1/', views.MensWear1.as_view(), name="menswear1"),
    path('menswear2/', views.MensWear2.as_view(), name="menswear2"),
    path('menswear3/', views.MensWear3.as_view(), name="menswear3"),
    path('menswear4/', views.MensWear4.as_view(), name="menswear4"),

    path('womenswear/', views.WoMensWear.as_view(), name="womenswear"),
    path('womenswear1/', views.WoMensWear1.as_view(), name="womenswear1"),
    path('womenswear2/', views.WoMensWear2.as_view(), name="womenswear2"),
    path('womenswear3/', views.WoMensWear3.as_view(), name="womenswear3"),
    path('womenswear4/', views.WoMensWear4.as_view(), name="womenswear4"),
    path('womenswear5/', views.WoMensWear5.as_view(), name="womenswear5"),
    path('womenswear6/', views.WoMensWear6.as_view(), name="womenswear6"),


    path('b1/', views.boy1.as_view(), name="b1"),
    path('b2/', views.boy2.as_view(), name="b2"),
    path('b3/', views.boy3.as_view(), name="b3"),
    path('g1/', views.girl1.as_view(), name="g1"),
    path('g2/', views.girl2.as_view(), name="g2"),
    path('g3/', views.girl3.as_view(), name="g3"),


    path('influencerhome/', views.InfluencerProductView.as_view(), name="influencerhome"),
    #path('login/', auth_views.LoginView.as_view(), name="login"),
    path('registration/', views.CustomerRegistrationView.as_view(), name="registration"),
    
    path('accounts/login/', views.loginpage, name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    #path('accounts/login/', views.CustomerLoginView.as_view(), name="login"),

    #path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('influencersignup/', views.influencer_signup, name='influencersignup'),
    path('influencerlogin/', views.influencer_login, name='influencerlogin'),

    #path('changepassword/', views.change_password, name='changepassword'),
    #path('passwordchange/', views.passwordchange, name='passwordchange'),


    # path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchange/', views.password_change_view, name='passwordchange'),
    path('passwordchange2/', views.influencer_password_change_view, name='influencerpasswordchange'),
    # path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('passwordchangedone/', views.password_change_done, name='passwordchangedone'),
    path('passwordchangedone2/', views.influencer_password_change_done, name='influencerpasswordchangedone'),


    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    # path('password-reset/', views.my_password_reset_view, name='password_reset'),





    #############TILL PASSWORD RESET#####################





    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'), 

    path('influencer-product-detail/<int:pk>', views.InfluencerProductDetailView.as_view(), name='influencer-product-detail'), 

    path('influencer2-product-detail/<int:pk>', views.Influencer2ProductDetailView.as_view(), name='influencer2-product-detail'), 



    path('add-to-cart/', views.add_to_cart, name='cart'),

    path('buy/', views.buynow, name='buy'),

    path('returnpro/', views.returnpro, name='returnpro'),


    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),

    path('x-page/<str:influencercode>/', views.x_page, name='x_page'),




    #path('buy/', views.buy_now, name='buy-now'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'), 

    path('influencer-add-to-cart/', views.influencercart, name='influencer-cart'),
    path('influencercart/', views.showinfluencercart, name='showinfluencercart'),
    path('influencerremovecart/', views.influencer_remove_cart, name='influencerremovecart'),

    path('search/', views.search, name='search'),
    path('getcode/', views.insta, name='getcode'),



    path('addProductbysellerjgvjbhj/', views.addProduct, name="addproduct"),
    path('delProduct/<id>/', views.delete_Product, name="delproduct"),

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)