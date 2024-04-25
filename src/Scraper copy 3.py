from lib.imports import *
from lib.page import *
from lib.resources import *
from lib.Driver import *    
import os
import time
import logging
import re

def main():
    url = "https://www.fragrancedirect.co.uk/fragrance/mens-fragrance/shop-all.list"
    driver = initialize_and_navigate(url)
    action_chains = ActionChains(driver)
    
    actions = ActionChains(driver)
    csvv = HomePage(driver)
    csvv.make_csv('fragrancedirect.csv', 'Title,Price,updated price,weight,Product overview,Range,Brand,Volume,URL\n')
    csvv.make_csv('fragrancedirect_nonvarriant.csv', 'URL\n')

    current_page = 1
    next_button_xpath = '//*[@class="responsiveProductListPage_bottomPagination"]//button[@class="responsivePaginationNavigationButton paginationNavigationButtonNext"]'
    
    try:
        time.sleep(5)
        action_chains.send_keys(Keys.ESCAPE).perform()
        mainpagee = HomePage(driver)
        mainpagee.waiTENt(Fragrancess.Bar)
        barr = driver.find_element(By.XPATH, Fragrancess.Bar).click()
    except Exception as e:
        logging.warning(f"No bar found: {e}")

    main_folder = 'men_frag'
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
    
    while True:
        logging.info(f"Processing products on page {current_page}...")
    
        productts = driver.find_elements(By.XPATH, Fragrancess.Products)
        current_url = driver.current_url
        print(current_url)
        for product in productts:
            try:
                
                time.sleep(1)
                action_chains.key_down(Keys.CONTROL).perform()
                product.click()
                action_chains.key_up(Keys.CONTROL).perform()
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)
                    
                try:
                    varriantt = HomePage(driver)
                    varriantt.waiTENt(Fragrancess.varriaannt)
                    btns_varriant = driver.find_elements(By.XPATH, '//*[@id="mainContent"]//*[@class="athenaProductPage_productVariations productPage_productVariations_selector "]//li')
                    num_btns = len(btns_varriant)
                    time.sleep(5)
                    for x in range(1 ,num_btns + 1):
                        # (locator)[x]
                        btnx = driver.find_element(By.XPATH, f'(//*[@id="mainContent"]//*[@class="athenaProductPage_productVariations productPage_productVariations_selector "]//li)[{x}]')
                        
                        time.sleep(1)
                        try:
                            print("for test try")
                            action_chains.move_to_element(btnx).perform()
                            btnx.click()
                    
                        except:
                            print("for test exception")
                            driver.execute_script('arguments[0].click()', btnx)
                            
                        time.sleep(10)
                        product_titlee = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Fragrancess.varriant_title)))
                        print(product_titlee.text)
                        time.sleep(0.5)
                        product_rrp_text = ''
                        product_over_text = ''
                        product_range = ''
                        product_brand = ''
                        product_volume = ''
                        try:
                            product_rrp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Fragrancess.RRP)))
                            product_rrp_text = product_rrp.text.replace('RRP:', '').replace('$', '').strip()
                            print(product_rrp_text)
                        except:
                            logging.warning("RRP not found")

                        try:
                            product_over = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Fragrancess.PRODUCTover)))
                            product_over_text = product_over.text.replace('"', '""').strip()
                            print(product_over_text)
                        except:
                            logging.warning("Product overview not found")
                        
                        
                        time.sleep(0.5)
                        product_deta = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Fragrancess.Varriant_product_detailll)))
                        action_chains.move_to_element(product_deta).perform()
                        time.sleep(0.5)
                        product_detaill = HomePage(driver)
                        product_detaill.click_btn(Fragrancess.Varriant_product_detailll)
                        time.sleep(0.5)

                        try:
                            # product_range_element = driver.find_element(By.XPATH, Fragrancess.RANGE)
                            product_range_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Fragrancess.Varraint_RANGE)))
                            product_range = product_range_element.text.replace('"', '""').strip() if product_range_element else ''
                            print(product_range)
                        except:
                            logging.warning("Range not found")

                        try:
                            # product_brand_element = driver.find_element(By.XPATH, Fragrancess.BRAND)
                            product_brand_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Fragrancess.varriant_BRAND)))
                            product_brand = product_brand_element.text.replace('"', '""').strip() if product_brand_element else ''
                            print(product_brand)
                        except:
                            logging.warning("Brand not found")

                        try:
                            # product_volume_element = driver.find_element(By.XPATH, Fragrancess.VOLUME)
                            product_volume_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Fragrancess.Varriant_VOLUME)))
                            product_volume = product_volume_element.text.replace('"', '""').strip() if product_volume_element else ''
                            print(product_volume)
                        except:
                            logging.warning("Volume not found")
                        try:
                            
                            if product_brand in product_titlee.text:
                                updated_title = product_titlee.text.replace(product_brand, '').strip()
                        except:
                            updated_title = "brand not found"
                        
                        product_price = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Fragrancess.RRP)))
                        product_price_text = product_price.text.replace('RRP:', '').replace('£', '').strip()
                        updated_price = float(product_price_text) * 1.7
                        print(updated_price)

                        weight_match = re.search(r'(\d+ml|\d+ ml)', product_titlee.text, re.IGNORECASE)
                        weight = weight_match.group(1).strip() if weight_match else ''
                        print(weight)
                        current_url = driver.current_url
                        print(current_url)
                        csvv.make_csv('fragrancedirect.csv', f'"{product_titlee.text}","{product_rrp_text}","{updated_price}","{weight}","{product_over_text}","{product_range}","{product_brand}","{product_volume}",{current_url},', new=False)
                        image_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="athenaProductImageCarousel_thumbnailScrollContainer "]//ul/li//img')))
                        for img in image_elements:
                            img_url = img.get_attribute('src')
                            if img_url.startswith('http'):
                                new_img_url = img_url.replace('/130/130/', '/512/512/')
                                csvv.make_csv('fragrancedirect.csv', f'"{new_img_url}",', new=False)
                            else:
                                logging.warning(f"Invalid image URL: {img_url}")
                        csvv.make_csv('fragrancedirect.csv', '\n', new=False)
                        time.sleep(2)
                    time.sleep(2)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                except:
                    current_url = driver.current_url
                    print(current_url)
                    csvv.make_csv('fragrancedirect_nonvarriant.csv', f'"{current_url}",', new=False)
                    continue
                    
            except Exception as e:     
                current_url = driver.current_url
                print(current_url)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                logging.error(f"Error processing product on page {current_page}: {e}")
                    
        if not navigate_to_next_page(driver, next_button_xpath):
            logging.info(f"No more pages available. Finished processing.")
            break   

        current_page += 1
        time.sleep(5)

    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()
                        
                            
#                 except Exception as e:
#                     # print(e)
#                     time.sleep(1)
#                     product_titlee = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Fragrancess.Title)))
#                     print(product_titlee.text)
#                     time.sleep(1)
#                     driver.close()
#                     driver.switch_to.window(driver.window_handles[0])

#                 time.sleep(1)
#                 driver.close()
#                 driver.switch_to.window(driver.window_handles[0])

#             except Exception as e:     
#                 current_url = driver.current_url
#                 print(current_url)
#                 driver.close()
#                 driver.switch_to.window(driver.window_handles[0])
#                 logging.error(f"Error processing product on page {current_page}: {e}")
#         if not navigate_to_next_page(driver, next_button_xpath):
#             logging.info(f"No more pages available. Finished processing.")
#             break   

#         current_page += 1
#         time.sleep(5)

#         time.sleep(10)
#         driver.quit()

# if __name__ == "__main__":
#     main()
