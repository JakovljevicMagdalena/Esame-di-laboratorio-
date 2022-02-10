import datetime

class ExamException(Exception): #classe per le eccezioni
    pass

class CSVFile:

    def __init__(self, name):
        self.name = name      
        # Provo ad aprirlo e leggere una riga
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.can_read = False
            print('Error in reading file: "{}"'.format(e))


    def get_data(self):
        if not self.can_read:
            print('Error, file not open or unreadable')
            return None

        else:
            data = []
    
            # Apro il file
            my_file = open(self.name, 'r')
            # Leggo il file linea per linea
            for line in my_file:
                 # Faccio lo split di ogni linea sulla virgola
                elements = line.split(',')
                 # Se NON sto processando l'intestazione...
                if elements[0] != 'Date':
                    # Aggiungo alla lista gli elementi di questa linea
                    data.append(elements)
            
            # Chiudo il file
            my_file.close()
            
            # Quando ho processato tutte le righe, ritorno i dati
            return data


class CSVTimeSeriesFile:
    time_series = []
    def __init__(self, name ):
      self.name=name

      if not isinstance(name, str):
         raise ExamException("Error: parameter 'name' must be a string and not {type (name)}")   
         pass #la funzione isistance() mi permette di verificare se un oggetto è un'istanza di una classe
      
       
    def get_data(self): 
      temp = []
      one = True 
      two = False

      try:
            my_file = open(self.name, 'r') #provo ad aprire il file 
      
      except(FileNotFoundError):
            raise ExamException('Error, error in reading file') 
      
      for line in my_file:
        temp = []
        element = line.split(",") 

        if len(element)!=2:
          continue
        cur_time = element[0]

        try:
          date_2 = datetime.datetime.strptime(cur_time, "%Y-%M") #Il modulo datetime include le funzioni e le classi per analizzare, formattare e compiere operazioni aritmetiche su date e orari
          if one:  
            last_time = cur_time
            one = False 
          date_1 = datetime.datetime.strptime(last_time, "%Y-%M") #formato (anno - mese)(year - month)
        except(ValueError): 
          continue 

        if date_1 > date_2:
          raise ExamException('Error, wrong sequence of dates')

        if date_1 == date_2 and two:
          raise ExamException('Error, duplicate dates')
        temp.append(cur_time)

        try: 
          temp.append(float(element[1]))
        except(ValueError): 
          continue 

        if temp[1] <= 0:
          continue
        
        self.time_series.append(temp)

      my_file.close()
      return self.time_series



def compute_avg_monthly_difference (time_series, first_year, last_year): #funzione a sé stante, per calcolare la differenza media del numero di passeggeri mensile tra anni consecutivi

  begging_year=int(first_year)
  ending_year=int(last_year)
  years=[]
  year_record=[]
  number_of_years = ending_year -  begging_year

  if ( number_of_years <= 0):
    raise ExamException('Error, wrong range of years') 

  for i in time_series:
    temp_date = i[0].split("-")
    year_current = int(temp_date[0])

    if year_current not in year_record:
      year_record.append(year_current)

  if (begging_year not in year_record) and (ending_year not in year_record):
    raise ExamException('Error, years are out of range')

  for i in range(number_of_years + 1):
    temp = []
    for j in range(12):
      temp.append(-1)
    years.append(temp)
    
  for i in time_series: 
    temp_date = i[0].split("-")
    year_current = int(temp_date[0])
    if (year_current >= begging_year) and (year_current<= ending_year):
      year_position = (begging_year - year_current)*-1 
      month_position= int(temp_date[1])-1
      years[year_position][month_position]=i[1]
  
  

  average=[]
  for i in range(12):
    temp=0
    no_years = number_of_years
    last_valid = 0

    for j in range(number_of_years + 1):
      if (years[j][i] != -1):
        last_valid = j 
        break 

    for j in range(number_of_years + 1):
      if (years[j][i] != -1):
        temp_2= years[j][i] - years[last_valid][i]
        temp = temp + temp_2
        last_valid = j 
      else: 
        no_years = no_years - 1 

    if (no_years <= 0):
      average.append(0)
    else:
      average.append(temp/no_years)
  return(average)
  

time_series_file = CSVTimeSeriesFile (name = 'Data.csv') 
time_series = time_series_file.get_data()    
risultato=compute_avg_monthly_difference (time_series, "1949", "1951")
print(risultato)
