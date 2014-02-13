class UsersController < ApplicationController

  def add
    if params[:name].length == 0
	  render :json => { errCode: -3, counter: 1 } #ERR_BAD_USERNAME
    elsif params[:name].length >= 128
	  render :json => { errCode: -3, counter: 1 } #ERR_BAD_USERNAME
	elsif User.find_by_name(params[:name].downcase) != nil
	  render :json => { errCode: -2, counter: 1 } #ERR_USER_EXISTS
	elsif params[:password].length >= 128
	  render :json => { errCode: -4, counter: 1 } #ERR_BAD_PASSWORD
	else
	  @user = User.new(name:params[:name].downcase, password:params[:password], count:1)
	  @user.save
	  render :json => { errCode: 1, counter: 1 } #SUCCESS
	end
  end

  def login
    if params[:name].length == 0
	  render :json => { errCode: -3, counter: 1 } #ERR_BAD_USERNAME
    elsif params[:name].length >= 128
	  render :json => { errCode: -3, counter: 1 } #ERR_BAD_USERNAME
	elsif User.find_by_name(params[:name].downcase) == nil
	  render :json => { errCode: -1, counter: 1 } #ERR_BAD_CREDENTIALS
	elsif params[:password] != User.find_by_name(params[:name].downcase).password
	  render :json => { errCode: -1, counter: 1 } #ERR_BAD_CREDENTIALS
	else
	  @user = User.find_by_name(params[:name].downcase)
	  @user.counter = @user.counter + 1
	  @user.save
	  render :json => { errCode: 1, counter: 1 } #SUCCESS
	end
  end
  
  def reset
    users.destroy_all()
    render :json => { errCode: 1, counter: 1 } #SUCCESS
  end
  
  def tests
  end
  
end
