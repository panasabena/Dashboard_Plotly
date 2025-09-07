"""
Análisis Avanzado de Datos de Telecomunicaciones
Script complementario para análisis detallado y generación de insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class TelecomAnalyzer:
    def __init__(self, data_path):
        """Inicializar el analizador con los datos"""
        self.df = pd.read_csv(data_path)
        self.prepare_data()
        
    def prepare_data(self):
        """Preparar y limpiar los datos"""
        # Convertir variables booleanas
        self.df['International plan'] = self.df['International plan'].map({'Yes': 1, 'No': 0})
        self.df['Voice mail plan'] = self.df['Voice mail plan'].map({'Yes': 1, 'No': 0})
        self.df['Churn'] = self.df['Churn'].map({True: 1, False: 0})
        
        # Crear variables derivadas
        self.df['Total minutes'] = (self.df['Total day minutes'] + 
                                   self.df['Total eve minutes'] + 
                                   self.df['Total night minutes'])
        
        self.df['Total calls'] = (self.df['Total day calls'] + 
                                 self.df['Total eve calls'] + 
                                 self.df['Total night calls'])
        
        self.df['Total charges'] = (self.df['Total day charge'] + 
                                   self.df['Total eve charge'] + 
                                   self.df['Total night charge'])
        
        self.df['Avg minutes per call'] = self.df['Total minutes'] / self.df['Total calls']
        self.df['Avg charge per minute'] = self.df['Total charges'] / self.df['Total minutes']
        
    def get_basic_stats(self):
        """Obtener estadísticas básicas"""
        stats = {
            'total_customers': len(self.df),
            'churn_rate': self.df['Churn'].mean() * 100,
            'avg_account_length': self.df['Account length'].mean(),
            'avg_customer_service_calls': self.df['Customer service calls'].mean(),
            'international_plan_rate': self.df['International plan'].mean() * 100,
            'voice_mail_plan_rate': self.df['Voice mail plan'].mean() * 100
        }
        return stats
    
    def analyze_churn_factors(self):
        """Analizar factores que influyen en el churn"""
        factors = {}
        
        # Análisis por plan internacional
        intl_churn = self.df.groupby('International plan')['Churn'].agg(['mean', 'count'])
        factors['international_plan'] = {
            'churn_rate_with_plan': intl_churn.loc[1, 'mean'] * 100,
            'churn_rate_without_plan': intl_churn.loc[0, 'mean'] * 100,
            'customers_with_plan': intl_churn.loc[1, 'count'],
            'customers_without_plan': intl_churn.loc[0, 'count']
        }
        
        # Análisis por buzón de voz
        vmail_churn = self.df.groupby('Voice mail plan')['Churn'].agg(['mean', 'count'])
        factors['voice_mail_plan'] = {
            'churn_rate_with_plan': vmail_churn.loc[1, 'mean'] * 100,
            'churn_rate_without_plan': vmail_churn.loc[0, 'mean'] * 100,
            'customers_with_plan': vmail_churn.loc[1, 'count'],
            'customers_without_plan': vmail_churn.loc[0, 'count']
        }
        
        # Análisis por llamadas a servicio al cliente
        service_calls_churn = self.df.groupby('Customer service calls')['Churn'].mean()
        factors['customer_service_calls'] = service_calls_churn.to_dict()
        
        return factors
    
    def analyze_usage_patterns(self):
        """Analizar patrones de uso"""
        patterns = {}
        
        # Análisis por período del día
        periods = ['day', 'eve', 'night']
        for period in periods:
            minutes_col = f'Total {period} minutes'
            calls_col = f'Total {period} calls'
            charge_col = f'Total {period} charge'
            
            patterns[period] = {
                'avg_minutes': self.df[minutes_col].mean(),
                'avg_calls': self.df[calls_col].mean(),
                'avg_charge': self.df[charge_col].mean(),
                'churn_by_usage': self.df.groupby(pd.qcut(self.df[minutes_col], 4))['Churn'].mean().to_dict()
            }
        
        return patterns
    
    def analyze_geographic_patterns(self):
        """Analizar patrones geográficos"""
        geo_analysis = self.df.groupby('State').agg({
            'Churn': ['mean', 'count'],
            'Account length': 'mean',
            'Customer service calls': 'mean',
            'Total charges': 'mean'
        }).round(3)
        
        geo_analysis.columns = ['churn_rate', 'customer_count', 'avg_account_length', 
                               'avg_service_calls', 'avg_total_charges']
        
        return geo_analysis.sort_values('churn_rate', ascending=False)
    
    def build_churn_model(self):
        """Construir modelo predictivo de churn"""
        # Seleccionar features
        features = ['Account length', 'International plan', 'Voice mail plan',
                   'Number vmail messages', 'Total day minutes', 'Total day calls',
                   'Total day charge', 'Total eve minutes', 'Total eve calls',
                   'Total eve charge', 'Total night minutes', 'Total night calls',
                   'Total night charge', 'Total intl minutes', 'Total intl calls',
                   'Total intl charge', 'Customer service calls']
        
        X = self.df[features]
        y = self.df['Churn']
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Escalar datos
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Entrenar modelo
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train_scaled, y_train)
        
        # Evaluar modelo
        y_pred = rf_model.predict(X_test_scaled)
        
        # Obtener importancia de features
        feature_importance = pd.DataFrame({
            'feature': features,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return {
            'model': rf_model,
            'scaler': scaler,
            'feature_importance': feature_importance,
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
    
    def generate_insights(self):
        """Generar insights clave"""
        stats = self.get_basic_stats()
        factors = self.analyze_churn_factors()
        
        insights = {
            'key_metrics': stats,
            'risk_factors': {
                'international_plan_risk': factors['international_plan']['churn_rate_with_plan'] > 
                                         factors['international_plan']['churn_rate_without_plan'],
                'voice_mail_protection': factors['voice_mail_plan']['churn_rate_with_plan'] < 
                                        factors['voice_mail_plan']['churn_rate_without_plan'],
                'service_calls_threshold': max(factors['customer_service_calls'].keys())
            },
            'recommendations': [
                "Los clientes con planes internacionales tienen mayor riesgo de churn",
                "El buzón de voz parece ser un factor protector contra el churn",
                f"La tasa de churn general es del {stats['churn_rate']:.1f}%",
                f"El promedio de antigüedad es de {stats['avg_account_length']:.0f} días"
            ]
        }
        
        return insights

def main():
    """Función principal para ejecutar análisis"""
    print("🔍 Iniciando Análisis Avanzado de Datos de Telecomunicaciones")
    print("=" * 60)
    
    # Analizar ambos datasets
    datasets = {
        'Dataset Pequeño': 'Data/churn-bigml-20.csv',
        'Dataset Grande': 'Data/churn-bigml-80.csv'
    }
    
    for name, path in datasets.items():
        print(f"\n📊 Analizando {name}")
        print("-" * 40)
        
        try:
            analyzer = TelecomAnalyzer(path)
            
            # Estadísticas básicas
            stats = analyzer.get_basic_stats()
            print(f"📈 Estadísticas Básicas:")
            print(f"   • Total de clientes: {stats['total_customers']:,}")
            print(f"   • Tasa de churn: {stats['churn_rate']:.1f}%")
            print(f"   • Antigüedad promedio: {stats['avg_account_length']:.0f} días")
            print(f"   • Llamadas a servicio promedio: {stats['avg_customer_service_calls']:.1f}")
            
            # Factores de churn
            factors = analyzer.analyze_churn_factors()
            print(f"\n⚠️  Factores de Churn:")
            print(f"   • Plan Internacional - Con plan: {factors['international_plan']['churn_rate_with_plan']:.1f}%")
            print(f"   • Plan Internacional - Sin plan: {factors['international_plan']['churn_rate_without_plan']:.1f}%")
            print(f"   • Buzón de Voz - Con plan: {factors['voice_mail_plan']['churn_rate_with_plan']:.1f}%")
            print(f"   • Buzón de Voz - Sin plan: {factors['voice_mail_plan']['churn_rate_without_plan']:.1f}%")
            
            # Insights
            insights = analyzer.generate_insights()
            print(f"\n💡 Insights Clave:")
            for rec in insights['recommendations']:
                print(f"   • {rec}")
            
            # Modelo predictivo
            print(f"\n🤖 Construyendo Modelo Predictivo...")
            model_results = analyzer.build_churn_model()
            print(f"   • Features más importantes:")
            top_features = model_results['feature_importance'].head(5)
            for _, row in top_features.iterrows():
                print(f"     - {row['feature']}: {row['importance']:.3f}")
            
        except Exception as e:
            print(f"❌ Error analizando {name}: {str(e)}")
    
    print(f"\n✅ Análisis completado!")
    print("=" * 60)

if __name__ == "__main__":
    main()
