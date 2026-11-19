"""12주차 성적 데이터 분석."""
from pathlib import Path
import pandas as pd


def 정제(df):
    df = df.copy()
    print('시작', len(df))
    df = df.dropna(subset=['점수']).copy()
    print('빈 칸 제거', len(df))
    df = df.drop_duplicates().copy()
    print('중복 제거', len(df))
    df['반'] = df['반'].str.strip()
    df['과목'] = df['과목'].str.strip()
    df = df[df['점수'].between(0, 100)].copy()
    print('범위 밖 제거', len(df))
    return df


def 수학필터(df):
    result = df[df['과목'] == '수학'].copy()
    print('수학 행 수', len(result))
    return result


def 반별평균(df):
    return df.groupby('반')['점수'].mean()


def 과목반별평균(df):
    return df.groupby(['과목', '반'])['점수'].mean()


def 반별통계(df):
    return df.groupby('반')['점수'].agg(개수='count', 평균='mean', 중앙값='median', 최댓값='max').round(2)


if __name__ == '__main__':
    folder = Path(__file__).resolve().parent
    raw = pd.read_csv(folder / 'scores_2026.csv')
    print('원본 크기', raw.shape)
    print('점수 결측', raw['점수'].isna().sum())
    print('완전 중복', raw.duplicated().sum())
    print('반 종류', raw['반'].unique())
    print('과목 종류', raw['과목'].unique())
    print('최솟값/최댓값', raw['점수'].min(), raw['점수'].max())
    clean = 정제(raw)
    수학필터(clean)
    print('반별 평균\n', 반별평균(clean))
    print('과목·반별 평균\n', 과목반별평균(clean))
    print('반별 통계\n', 반별통계(clean))
    print('전체 합계', clean['점수'].sum())
    print('그룹 합계', clean.groupby('반')['점수'].sum().sum())
